import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from celery import Celery
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import JWTManager, create_access_token, get_jwt
#BASIC APP SETUP
import csv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from celery import Celery
from celery.result import AsyncResult
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)

# EMAIL CONFIG

#EMAIL_USER = "lazyiitians17@gmail.com"
#EMAIL_PASS = "fbwb fcgb tibh mlpg"


#CELERY SETUP
# CELERY SETUP
def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(
        broker_url="redis://localhost:6379/0",
        result_backend="redis://localhost:6379/0",
        task_track_started=True,
        result_expires=3600
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

#CELERY BEAT SCHEDULE 
celery.conf.beat_schedule = {
    "send-report": {
        "task": "app.send_company_reports_task",
        "schedule": 60.0
    },
    "reminder": {
        "task": "app.interview_reminder_job",
        "schedule": 60.0
    }
}


from flask_caching import Cache

# cache config (using same redis)
app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/1"  # use diff db than celery

cache = Cache(app)
#models

class SystemUser(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    email_address = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)
    contact = db.Column(db.String(15))

    gender = db.Column(db.String(20))
    system_user_role = db.Column(db.String(20), nullable=False)

    approve = db.Column(db.Boolean, default=False)
    is_blacklisted = db.Column(db.Boolean, default=False)

    create = db.Column(db.DateTime, default=datetime.utcnow)

    stu_profile = db.relationship("StudentProfile", back_populates="user")

    comp_profile = db.relationship("CompanyProfile", back_populates="user")


class StudentProfile(db.Model):
    __tablename__ = "student_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    department = db.Column(db.String(100))

    studentName = db.Column(db.String(150))
    cgpa = db.Column(db.Float)

    resume = db.Column(db.String(200))

    education = db.Column(db.String(200))
    skills = db.Column(db.Text)

    user = db.relationship("SystemUser", back_populates="stu_profile")

    applications = db.relationship("Application", back_populates="student")

    placement = db.relationship("Placement", back_populates="student", uselist=False)


class CompanyProfile(db.Model):

    __tablename__ = "company_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    company_name = db.Column(db.String(150))
    industry = db.Column(db.String(100))

    website = db.Column(db.String(150))
    des = db.Column(db.Text)

    location = db.Column(db.String(100))
    comp_size = db.Column(db.String(50))

    user = db.relationship("SystemUser", back_populates="comp_profile")
    jobs = db.relationship("Job", back_populates="company")
    placements = db.relationship("Placement", back_populates="company")


class Job(db.Model):

    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(db.Integer, db.ForeignKey("company_profiles.id"))

    title = db.Column(db.String(150))

    desc = db.Column(db.Text)
    skills_req = db.Column(db.String(200))

    salary = db.Column(db.String(50))
    job_type = db.Column(db.String(50))

    eligibility = db.Column(db.Text)
    deadline = db.Column(db.Date)
    approve = db.Column(db.Boolean, default=False)

    closed = db.Column(db.Boolean, default=False)
    create = db.Column(db.DateTime, default=datetime.utcnow)


    company = db.relationship("CompanyProfile", back_populates="jobs")
    applications = db.relationship("Application", back_populates="job")


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))

    student_id = db.Column(db.Integer, db.ForeignKey("student_profiles.id"))
    status = db.Column(db.String(50), default="Applied")

    apply = db.Column(db.DateTime, default=datetime.utcnow)

    job = db.relationship("Job", back_populates="applications")
    student = db.relationship("StudentProfile", back_populates="applications")

    placement = db.relationship("Placement", back_populates="application", uselist=False)


class Placement(db.Model):

    __tablename__ = "placements"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey("student_profiles.id"), nullable=False)

    company_id = db.Column(db.Integer, db.ForeignKey("company_profiles.id"), nullable=False)

    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))

    application_id = db.Column(db.Integer, db.ForeignKey("applications.id"))
    position = db.Column(db.String(150))
    salary = db.Column(db.String(50))

    joining_date = db.Column(db.Date)
    placed_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship("StudentProfile", back_populates="placement")
    company = db.relationship("CompanyProfile", back_populates="placements")

    application = db.relationship("Application", back_populates="placement")

# ---------------- CELERY TASKS ----------------

@celery.task(name="app.interview_reminder_job")
def interview_reminder_job():
    print("running reminder...")

    applications = Application.query.filter_by(status="Shortlisted").all()
    if not applications:
        print("no shortlisted applications")
        return

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)

    for app_obj in applications:
        if not app_obj.student or not app_obj.student.user:
            continue

        email = app_obj.student.user.email_address
        name = app_obj.student.user.name
        company_name = app_obj.job.company.company_name if app_obj.job else ""
        role = app_obj.job.title if app_obj.job else ""

        msg = MIMEMultipart()
        msg["Subject"] = "Interview Update"
        msg["From"] = EMAIL_USER
        msg["To"] = email
        msg.attach(MIMEText(f"""
Hello {name},

You are shortlisted!

Company: {company_name}
Role: {role}

Good luck!
""", "plain"))

        server.sendmail(EMAIL_USER, email, msg.as_string())
        print("reminder sent:", email)

    server.quit()


@celery.task(name="app.send_company_reports_task")
def send_company_reports_task():
    print("running send reports...")

    companies = CompanyProfile.query.all()
    if not companies:
        print("no companies found")
        return

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)

    for company in companies:
        if not company.user:
            continue

        applications = Application.query.join(Job).filter(
            Job.company_id == company.id
        ).all()

        lines = [f"Placement Report for {company.company_name}", ""]
        for app_obj in applications:
            student = app_obj.student
            job = app_obj.job
            name = student.user.name if student and student.user else "Unknown"
            title = job.title if job else "Unknown"
            lines.append(f"{name} - {title} - {app_obj.status}")

        msg = MIMEMultipart()
        msg["Subject"] = "Placement Report"
        msg["From"] = EMAIL_USER
        msg["To"] = company.user.email_address
        msg.attach(MIMEText("\n".join(lines), "plain"))

        server.sendmail(EMAIL_USER, company.user.email_address, msg.as_string())
        print("report sent:", company.user.email_address)

    server.quit()


@celery.task(name="app.export_student_apps")
def export_student_apps(student_id):
    print(f"exporting apps for student {student_id}...")

    os.makedirs("exports", exist_ok=True)
    path = f"exports/student_{student_id}.csv"

    apps = Application.query.filter_by(student_id=student_id).all()

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Job", "Company", "Status"])
        for a in apps:
            writer.writerow([
                a.job.title if a.job else "",
                a.job.company.company_name if a.job else "",
                a.status
            ])

    print("student export created:", path)
    return path


@celery.task(name="app.generate_company_report_task")
def generate_company_report_task(company_id):
    print(f"generating report for company {company_id}...")

    os.makedirs("reports", exist_ok=True)
    filename = f"company_{company_id}_report.csv"
    filepath = os.path.join("reports", filename)

    applications = Application.query.join(Job).filter(
        Job.company_id == company_id
    ).all()

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Company Report"])
        writer.writerow(["Company ID", company_id])
        writer.writerow(["Generated", datetime.now()])
        writer.writerow([])
        writer.writerow(["Student Name", "Email", "Job", "Status"])

        for app_obj in applications:
            student = app_obj.student
            job = app_obj.job
            writer.writerow([
                student.user.name if student and student.user else "",
                student.user.email_address if student and student.user else "",
                job.title if job else "",
                app_obj.status
            ])

    print("company report generated:", filename)
    return filename


@celery.task(name="app.generate_admin_report_task")
def generate_admin_report_task():
    print("generating admin full report...")

    os.makedirs("reports", exist_ok=True)
    filename = "admin_full_report.csv"
    filepath = os.path.join("reports", filename)

    applications = Application.query.all()

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Full Placement Report"])
        writer.writerow(["Generated", datetime.now()])
        writer.writerow([])
        writer.writerow(["Student Name", "Email", "Company", "Job", "Status", "Applied On"])

        for app_obj in applications:
            student = app_obj.student
            job = app_obj.job
            company = job.company if job else None
            writer.writerow([
                student.user.name if student and student.user else "",
                student.user.email_address if student and student.user else "",
                company.company_name if company else "",
                job.title if job else "",
                app_obj.status,
                app_obj.apply.strftime("%d-%m-%Y") if app_obj.apply else ""
            ])

    print("admin report generated:", filename)
    return filename


# ---------------- REPORT ROUTES - COMPANY ----------------

@app.route("/company/generate-report", methods=["GET"])
@jwt_required()
def generate_company_report_api():
    user_id = get_jwt_identity()
    user = SystemUser.query.get(int(user_id))

    if not user.comp_profile:
        return jsonify({"error": "Company not found"}), 404

    company = user.comp_profile[0]
    task = generate_company_report_task.delay(company.id)

    return jsonify({
        "message": "Company report started",
        "task_id": task.id
    }), 202


@app.route("/company/report-status/<task_id>", methods=["GET"])

def get_company_report_status(task_id):
    task = AsyncResult(task_id, app=celery)

    if task.state == "SUCCESS":
        return jsonify({
            "status": "done",
            "download_url": f"/company/download-report/{task.result}"
        })
    elif task.state == "FAILURE":
        return jsonify({"status": "failed"})
    else:
        return jsonify({"status": "pending"})


@app.route("/company/download-report/<filename>", methods=["GET"])

def download_company_report(filename):
    return send_from_directory(
        directory="reports",
        path=filename,
        as_attachment=True
    )


# ---------------- REPORT ROUTES - ADMIN ----------------

@app.route("/admin/generate-report", methods=["GET"])
@jwt_required()
def admin_generate_report():
    user_id = get_jwt_identity()
    admin = SystemUser.query.get(int(user_id))

    if admin.system_user_role != "admin":
        return jsonify({"msg": "Admin access required"}), 403

    task = generate_admin_report_task.delay()

    return jsonify({
        "message": "Report generation started",
        "task_id": task.id
    }), 202


@app.route("/admin/report-status/<task_id>", methods=["GET"])
@jwt_required()
def get_admin_report_status(task_id):
    user_id = get_jwt_identity()
    admin = SystemUser.query.get(int(user_id))

    if admin.system_user_role != "admin":
        return jsonify({"msg": "Admin access required"}), 403

    task = AsyncResult(task_id, app=celery)

    if task.state == "SUCCESS":
        return jsonify({
            "status": "done",
            "download_url": f"/admin/download-report/{task.result}"
        })
    elif task.state == "FAILURE":
        return jsonify({"status": "failed"})
    else:
        return jsonify({"status": "pending"})


@app.route("/admin/download-report/<filename>", methods=["GET"])
@jwt_required()
def admin_download_report(filename):
    return send_from_directory(
        directory="reports",
        path=filename,
        as_attachment=True
    )








@app.route("/registration", methods=["POST"])
def registration():
    data = request.get_json()

    if not data:

        return jsonify({"message": "No data provided"}), 400

    name = data.get("name")
    email = data.get("email_address")
    password = data.get("password")

    contact = data.get("contact")
    gender = data.get("gender")

    role = data.get("system_user_role")

    # saare requirad fields check kro

    if not name or not email or not password or not role:

        return jsonify({"message": "All required fields are needed"}), 400

    # admin khud register nhi kr skta
    if role.lower() == "admin":

        return jsonify({"message": "Admin registration not allowed"}), 403

    # pehle se exist krta h kya

    user = SystemUser.query.filter_by(email_address=email).first()

    if user:
        return jsonify({"message": "User already exists"}), 400

    new_user = SystemUser(
        name=name,
        email_address=email,
        password=password,
        contact=contact,
        gender=gender,
        system_user_role=role.lower(),

        approve=False if role.lower() == "company" 
        else True       # company ko admin approve krega
    )
    db.session.add(new_user)
    db.session.commit()

    # student ka profile bhi bna do registretion pe hi
    if role.lower() == "student":

        student_profile = StudentProfile(user_id=new_user.id, studentName=new_user.name)
        db.session.add(student_profile)
        db.session.commit()

    return jsonify({"message": "Registration successful"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"msg": "No data provided"}), 400

    user = SystemUser.query.filter_by(email_address=data.get("email_address")).first()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    # password match krna
    if user.password != data.get("password"):
        return jsonify({"msg": "Wrong password"}), 401

    if user.is_blacklisted:
        return jsonify({"msg": "Your account has been blacklisted"}), 403

    # company approved h ya nhi
    if user.system_user_role == "company" and not user.approve:
        return jsonify({"msg": "Company not approved by admin yet"}), 403

    access_token = create_access_token(
        identity=str(user.id),

        additional_claims={"role": user.system_user_role, "email": user.email_address}
    )

    return jsonify({
        "msg": "Login successful",
        "token": access_token,

        "role": user.system_user_role,
        "user_id": user.id,
        "name": user.name
    }), 200



# comp

@app.route("/company_dashboard/company_profile", methods=["POST"])

@jwt_required()
def create_company_profile():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    # agar pehle se profile h toh update krdo

    existing = CompanyProfile.query.filter_by(user_id=user_id).first()

    if existing:
        existing.company_name = data.get("company_name", existing.company_name)
        existing.industry = data.get("industry", existing.industry)

        existing.website = data.get("website", existing.website)

        existing.location = data.get("location", existing.location)
        existing.comp_size = data.get("comp_size", existing.comp_size)

        existing.des = data.get("des", existing.des)
        db.session.commit()

        return jsonify({"message": "Company profile updated"}), 200

    company = CompanyProfile(
        user_id=user_id,
        company_name=data.get("company_name"),
        industry=data.get("industry"),
        website=data.get("website"),
        location=data.get("location"),
        comp_size=data.get("comp_size"),
        des=data.get("des")
    )
    db.session.add(company)
    db.session.commit()
    return jsonify({"message": "Company profile created"}), 201


@app.route("/company/profile", methods=["GET"])
@jwt_required()
def get_company_profile():
    user_id = int(get_jwt_identity())
    user = SystemUser.query.get(user_id)

    company = CompanyProfile.query.filter_by(user_id=user_id).first()

    # pro nhi bni abhi
    if not company:
        return jsonify({
            "company_name": user.name if user else "",
            "industry": "",
            "location": "",

            "website": "",
            "des": "",
            "comp_size": "",

            "has_profile": False
        }), 200

    return jsonify({
        "company_name": company.company_name
          or "",
        "industry": company.industry
          or "",
        "location": company.location 
        or "",
        "website": company.website
          or "",
        "des": company.des
          or "",


        "comp_size": company.comp_size 
        or "",
        "has_profile": True

    }), 200


@app.route("/company/jobs", methods=["GET"])
@jwt_required()
def get_company_jobs():
    user_id = int(get_jwt_identity())
    company = CompanyProfile.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"jobs": [], "company_name": "", "has_profile": False}), 200

    # latest jobs pehle dikhao
    jobs = Job.query.filter_by(company_id=company.id).order_by(Job.create.desc()).all()
    jobs_data = []

    for job in jobs:
        apps_count = Application.query.filter_by(job_id=job.id).count()
        jobs_data.append({
            "id": job.id,
            "title": job.title,

            "desc": job.desc,
            "skills_req": job.skills_req,
            "salary": job.salary,

            "job_type": job.job_type,
            "eligibility": job.eligibility,

            "deadline": job.deadline.strftime("%Y-%m-%d") 
            if job.deadline
            
            else "",
            "approve": job.approve,

            "closed": job.closed,
            "created_at": job.create.strftime("%d-%m-%Y") 
            if job.create else "",
            "applications_count": apps_count
        })

    return jsonify({
        "jobs": jobs_data,
        "company_name": company.company_name or "",
        "has_profile": True
    }), 200


@app.route("/create_job", methods=["POST"])
@jwt_required()
def create_job():
    data = request.get_json()
    user_id = int(get_jwt_identity())

    company = CompanyProfile.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"msg": "Company profile not found. Please create profile first."}), 404

    # ye teeno fields mandatory h
    if not data.get("title") or not data.get("job_type") or not data.get("deadline"):
        return jsonify({"msg": "Title, Job Type and Deadline are required"}), 400

    try:
        deadline = datetime.strptime(data["deadline"], "%Y-%m-%d").date()

    except:
        return jsonify({"msg": "Deadline format should be YYYY-MM-DD"}), 400

    new_job = Job(
        company_id=company.id,
        title=data.get("title"),
        desc=data.get("desc", ""),
        skills_req=data.get("skills_req", ""),

        salary=data.get("salary", ""),
        job_type=data.get("job_type"),
        eligibility=data.get("eligibility", ""),
        deadline=deadline
    )
    db.session.add(new_job)
    db.session.commit()
    return jsonify({"message": "Job posted successfully! Waiting for admin approval."}), 201


@app.route("/company/drive/<int:drive_id>/applications", methods=["GET"])
@jwt_required()
def company_drive_applications(drive_id):
    user_id = int(get_jwt_identity())
    company = CompanyProfile.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"msg": "Company not found"}), 404

    job = Job.query.get(drive_id)

    # dusri company ka drive nhi dekh skte
    if not job or job.company_id != company.id:
        return jsonify({"msg": "Unauthorized"}), 403

    apps = Application.query.filter_by(job_id=drive_id).all()
    result = []

    for app in apps:
        student = StudentProfile.query.get(app.student_id)
        student_user = SystemUser.query.get(student.user_id) if student else None
        result.append({
            "id": app.id,
            "student_name": student_user.name if student_user 
            else "Unknown",
            "student_email": student_user.email_address 
            if student_user
              else "",
            "department": student.department or "",
            "cgpa": student.cgpa or "",
            "skills": student.skills
              or "",
            "resume": student.resume
              or "",
            "status": app.status,

            "apply_date": app.apply.strftime("%d/%m/%Y") if app.apply else ""
        })

    return jsonify({"applications": result, "job_title": job.title}), 200


@app.route("/company/application/<int:app_id>/status", methods=["POST"])
@jwt_required()
def update_application_status(app_id):
    user_id = int(get_jwt_identity())
    company = CompanyProfile.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"msg": "Unauthorized"}), 403

    data = request.get_json()
    new_status = data.get("status")

    # sirf yahi 4 status valid h
    if new_status not in ["Applied", "Shortlisted", "Waitlisted", "Rejected"]:
        return jsonify({"msg": "Invalid status"}), 400

    app = Application.query.get(app_id)

    if not app:
        return jsonify({"msg": "Application not found"}), 404

    job = Job.query.get(app.job_id)

    if not job or job.company_id != company.id:
        return jsonify({"msg": "Unauthorized"}), 403

    app.status = new_status
    db.session.commit()
    return jsonify({"message": f"Status updated to {new_status}"}), 200


@app.route("/company/drive/<int:drive_id>/complete", methods=["POST"])
@jwt_required()
def company_complete_drive(drive_id):
    user_id = int(get_jwt_identity())
    company = CompanyProfile.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"msg": "Company profile not found"}), 404

    job = Job.query.get(drive_id)

    if not job or job.company_id != company.id:
        return jsonify({"msg": "Unauthorized"}), 403

    job.closed = True
    db.session.commit()
    return jsonify({"message": "Drive marked complete"}), 200


@app.route("/company/dashboard_stats", methods=["GET"])
@cache.cached(timeout=120)
@jwt_required()
def company_dashboard_stats():
    user_id = int(get_jwt_identity())
    company = CompanyProfile.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"total_jobs": 0, "total_applications": 0, "shortlisted": 0}), 200

    total_jobs = Job.query.filter_by(company_id=company.id).count()
    job_ids = [job.id for job in company.jobs]
    total_applications = Application.query.filter(Application.job_id.in_(job_ids)).count()

    shortlisted = Application.query.filter(
        Application.job_id.in_(job_ids), Application.status == "Shortlisted"
    ).count()

    return jsonify({
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "shortlisted": shortlisted
    })


# STU

@app.route("/student/jobs", methods=["GET"])
@jwt_required()
@cache.cached(timeout=60)  # cache for 60 sec

def get_jobs():
    # sirf open aur approved jobs dikhao
    jobs = Job.query.filter_by(closed=False, approve=True).all()
    result = []

    for job in jobs:
        company = CompanyProfile.query.get(job.company_id)

        if not company:
            continue

        company_user = SystemUser.query.get(company.user_id)

        # blacklisted company ki jobs nhi dikhani
        if company_user and company_user.is_blacklisted:
            continue

        result.append({
            "job_id": job.id,
            "title": job.title,
            "salary": job.salary,
            "deadline": job.deadline.strftime("%Y-%m-%d")
              if job.deadline 
              else "",
            "company_id": company.id,
            "company_name": company.company_name,
            "location": company.location or "",
            "skills_req": job.skills_req or "",
            "job_type": job.job_type or "",
        })

    return jsonify(result), 200


@app.route("/student/companies", methods=["GET"])
@jwt_required()
def get_companies():
    companies = CompanyProfile.query.all()
    result = []

    for company in companies:
        user = SystemUser.query.get(company.user_id)

        if not user or not user.approve or user.is_blacklisted:
            continue

        # sirf wahi company dikhao jiske active drives h
        active_jobs = Job.query.filter_by(company_id=company.id,
                                           approve=True, closed=False).count()

        if active_jobs > 0:
            result.append(
                {
                "company_id": company.id,
                "company_name": company.company_name or "Unknown",
                "industry": company.industry
                  or "",
                "location": company.location
                 or "",
            })

    return jsonify(result), 200


@app.route("/student/company/<int:id>", methods=["GET"])
@jwt_required()
def company_details(id):
    company = CompanyProfile.query.get(id)

    if not company:
        return jsonify({"msg": "Company not found"}), 404

    jobs = Job.query.filter_by(company_id=id, closed=False, approve=True).all()
    job_list = []

    for job in jobs:
        job_list.append({
            "id": job.id,
            "title": job.title,
            "desc": job.desc,
            "skills_req": job.skills_req,
            "salary": job.salary,
            "job_type": job.job_type,
            "eligibility": job.eligibility,
            "deadline": job.deadline.strftime("%Y-%m-%d") 
            if job.deadline
              else "",
            "location": company.location,
        }
        )

    return jsonify({
        "company_name": company.company_name,
        "industry": company.industry,
        "location": company.location,

        "website": company.website,
        "des": company.des,
        "comp_size": company.comp_size,

        "jobs": job_list
    })


@app.route("/student/apply/<int:job_id>", methods=["POST"])
@jwt_required()
def apply(job_id):
    user_id = int(get_jwt_identity())
    student = StudentProfile.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"msg": "Student profile not found"}), 404

    # pehle se apply kiya h kya iske liye
    already = Application.query.filter_by(job_id=job_id, student_id=student.id).first()

    if already:
        return jsonify({"msg": "Already Applied"}), 400

    new_app = Application(job_id=job_id, student_id=student.id, status="Applied")
    db.session.add(new_app)
    db.session.commit()
    return jsonify({"msg": "Applied Successfully"}), 201


@app.route("/student/applications", methods=["GET"])
@jwt_required()
def my_applications():
    user_id = int(get_jwt_identity())
    student = StudentProfile.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify([]), 200

    # latest application pehle
    apps = Application.query.filter_by(student_id=student.id).order_by(Application.apply.desc()).all()
    result = []

    for app in apps:
        job = Job.query.get(app.job_id)
        company = CompanyProfile.query.get(job.company_id) if job else None
        result.append({
            "app_id": app.id,
            "job_title": job.title if job else "Unknown",
            "job_id": app.job_id,
            "company_name": company.company_name 
            if company else "Unknown",
            "status": app.status,
            "date": app.apply.strftime("%d-%m-%Y") if app.apply
              else ""
        })

    return jsonify(result)


@app.route("/student/profile", methods=["GET"])
@jwt_required()
def student_profile():
    user_id = int(get_jwt_identity())
    user = SystemUser.query.get(user_id)
    student = StudentProfile.query.filter_by(user_id=user_id).first()

    if not user or not student:
        return jsonify({"msg": "Student not found"}), 404

    return jsonify({
        "name": user.name,
        "email": user.email_address,
        "studentName": student.studentName
          or user.name,
        "department": student.department or "",
        "cgpa": student.cgpa or "",
        "skills": student.skills
          or "",
        "education": student.education or "",
        "resume": student.resume 
        or ""
    }), 200


@app.route("/student/profile", methods=["PUT"])
@jwt_required()
def update_student_profile():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    student = StudentProfile.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"msg": "Student not found"}), 404

    # jo bhi bheja h woh update krdo
    student.department = data.get("department", student.department)
    student.cgpa = data.get("cgpa", student.cgpa)
    student.skills = data.get("skills", student.skills)
    student.education = data.get("education", student.education)
    student.resume = data.get("resume", student.resume)
    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200


# ADMIN 

@app.route("/admin/profile", methods=["GET"])
@jwt_required()
def admin_profile():
    user_id = int(get_jwt_identity())
    user = SystemUser.query.get(user_id)

    

    return jsonify({"name": user.name, "email": user.email_address})


@app.route("/admin/stats", methods=["GET"])
@jwt_required()
def admin_stats():
    user_id = int(get_jwt_identity())
    admin = SystemUser.query.get(user_id)

    if admin.system_user_role != "admin":
        return jsonify({"msg": "Admin access required"}), 403

    return jsonify({
        "total_companies": SystemUser.query.filter_by(system_user_role="company").count(),
        "total_students": SystemUser.query.filter_by(system_user_role="student").count(),
        "total_drives": Job.query.filter_by(closed=False).count(),

        "total_applications": Application.query.count(),
        "total_pending_jobs": Job.query.filter_by(approve=False, closed=False).count()
    })


@app.route("/admin/companies", methods=["GET"])
@jwt_required()
def get_all_companies():
    user_id = int(get_jwt_identity())
    admin = SystemUser.query.get(user_id)

    if admin.system_user_role != "admin":
        return jsonify({"msg": "Admin access required"}), 403

    companies_users = SystemUser.query.filter_by(system_user_role="company").all()
    result = []

    for user in companies_users:
        company = CompanyProfile.query.filter_by(user_id=user.id).first()
        result.append({
            "id": company.id if company else None,
            "user_id": user.id,
            "company_name": company.company_name if company else user.name,
            "email": user.email_address,
            "industry": company.industry 
            if company else "",
            "location": company.location
              if company else "",
            "approved": user.approve,
            "blacklisted": user.is_blacklisted
        })

    return jsonify(result)


@app.route("/admin/students", methods=["GET"])
@jwt_required()
def get_all_students():
    user_id = int(get_jwt_identity())
    admin = SystemUser.query.get(user_id)

    if admin.system_user_role != "admin":
        return jsonify({"msg": "Admin access required"}), 403

    students = StudentProfile.query.all()
    result = []

    for stu in students:
        user = SystemUser.query.get(stu.user_id)
        result.append({
            "id": stu.id,
            "user_id": stu.user_id,
            "name": user.name 
            if user
              else "",
            "email": user.email_address if user

              else "",
            "department": stu.department or "",
            "cgpa": stu.cgpa or "",
            "skills": stu.skills or "",
            "blacklisted": user.is_blacklisted 
            if user else False
        })

    return jsonify(result)


@app.route("/admin/pending-companies", methods=["GET"])
@jwt_required()
def get_pending_companies():
    user_id = int(get_jwt_identity())
    admin = SystemUser.query.get(user_id)

    if admin.system_user_role != "admin":
        return jsonify({"msg": "Admin access required"}), 403

    # jinhe abhi approve nhi kiya
    pending_users = SystemUser.query.filter_by(system_user_role="company", approve=False).all()
    result = []

    for user in pending_users:
        company = CompanyProfile.query.filter_by(user_id=user.id).first()
        result.append({
            "id": user.id,
            "company_name": company.company_name if company else user.name,
            "email": user.email_address,
            "industry": company.industry if company 
            else "",
            "location": company.location if company 
            
            else ""
        })

    return jsonify(result)


@app.route("/admin/approve-company/<int:user_id>", methods=["POST"])

@jwt_required()
def approve_company(user_id):
    admin_id = int(get_jwt_identity())
    admin = SystemUser.query.get(admin_id)

    if admin.system_user_role != "admin":
        return jsonify({"msg": "Admin access required"}), 403

    user = SystemUser.query.get(user_id)

    if not user or user.system_user_role != "company":
        return jsonify({"msg": "Company not found"}), 404

    user.approve = True
    db.session.commit()

    return jsonify({"message": "Company approved successfully"})


@app.route("/admin/toggle-blacklist/<int:user_id>", methods=["POST"])
@jwt_required()
def toggle_blacklist(user_id):
    admin_id = int(get_jwt_identity())
    admin = SystemUser.query.get(admin_id)

    if admin.system_user_role != "admin":
        return jsonify({"msg": "Admin access required"}), 403

    user = SystemUser.query.get(user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    user.is_blacklisted = not user.is_blacklisted

    # agar company blacklist hui toh uske saare drives band krdo

    if user.system_user_role == "company" and user.is_blacklisted:
        company = CompanyProfile.query.filter_by(user_id=user.id).first()

        if company:
            Job.query.filter_by(company_id=company.id, closed=False).update({"closed": True})

    db.session.commit()

    status = "blacklisted" if user.is_blacklisted else "removed from blacklist"
    return jsonify({"message": f"User {status} successfully", "blacklisted": user.is_blacklisted})


@app.route("/admin/pending-jobs", methods=["GET"])
@jwt_required()
def get_pending_jobs():
    user_id = int(get_jwt_identity())
    admin = SystemUser.query.get(user_id)

    if admin.system_user_role != "admin":
        return jsonify({"msg": "Admin access required"}), 403

    # jo jobs abhi approve nhi hui
    jobs = Job.query.filter_by(approve=False, closed=False).all()
    result = []

    for job in jobs:
        company = CompanyProfile.query.get(job.company_id)
        result.append({
            "id": job.id,
            "title": job.title,
            "salary": job.salary 
            or "",
            "job_type": job.job_type or "",
            "company_name": company.company_name if company 
            else "Unknown",
            "created_at": job.create.strftime("%d-%m-%Y") if job.create
              else ""
        })

    return jsonify(result), 200


@app.route("/admin/approve-job/<int:job_id>", methods=["POST"])
@jwt_required()
def approve_job(job_id):
    user_id = int(get_jwt_identity())
    admin = SystemUser.query.get(user_id)

    if admin.system_user_role != "admin":
        return jsonify({"msg": "Admin access required"}), 403

    job = Job.query.get(job_id)

    if not job:
        return jsonify({"msg": "Job not found"}), 404

    job.approve = True
    db.session.commit()
    return jsonify({"message": "Job approved"}), 200


@app.route("/admin/reject-job/<int:job_id>", methods=["DELETE"])
@jwt_required()
def reject_job(job_id):
    user_id = int(get_jwt_identity())
    admin = SystemUser.query.get(user_id)

    if admin.system_user_role != "admin":
        return jsonify({"msg": "Admin access required"}), 403

    job = Job.query.get(job_id)

    if not job:
        return jsonify({"msg": "Job not found"}), 404

    # job delete krne se pehle uski applications bhi hatao
    Application.query.filter_by(job_id=job_id).delete()
    db.session.delete(job)
    db.session.commit()
    return jsonify({"message": "Job rejected and deleted"}), 200


@app.route("/admin/ongoing-drives", methods=["GET"])
@jwt_required()
def get_ongoing_drives():
    user_id = int(get_jwt_identity())
    admin = SystemUser.query.get(user_id)

    if admin.system_user_role != "admin":
        return jsonify({"msg": "Admin access required"}), 403

    drives = Job.query.filter_by(closed=False).all()
    result = []

    for idx, drive in enumerate(drives, 1001):
        company = CompanyProfile.query.get(drive.company_id)
        apps_count = Application.query.filter_by(job_id=drive.id).count()
        result.append({
            "sr_no": idx,
            "id": drive.id,
            "drive_name": drive.title,
            "company_name": company.company_name 
            if company else "Unknown",
            "applications": apps_count,
            "approved": drive.approve
        })

    return jsonify(result)


@app.route("/admin/drive/<int:drive_id>", methods=["GET"])
@jwt_required()
def get_drive_details(drive_id):
    user_id = int(get_jwt_identity())
    admin = SystemUser.query.get(user_id)

    if admin.system_user_role != "admin":
        return jsonify({"msg": "Admin access required"}), 403

    drive = Job.query.get(drive_id)

    if not drive:
        return jsonify({"msg": "Drive not found"}), 404

    company = CompanyProfile.query.get(drive.company_id)

    return jsonify({
        "drive_name": drive.title,
        "job_title": drive.title,
        "description": drive.desc,
        "skills_required": drive.skills_req,
        "salary": drive.salary,
        "job_type": drive.job_type,
        "eligibility": drive.eligibility,
        "location": company.location 
        if company
          else "N/A",
        "company_name": company.company_name 
        if company 
        else "Unknown",
        "posted_date": drive.create.strftime("%d/%m/%Y") 
        if drive.create else "N/A",
        "deadline": drive.deadline.strftime("%d/%m/%Y") if drive.deadline else "N/A"
    })


@app.route("/admin/complete-drive/<int:drive_id>", methods=["POST"])
@jwt_required()
def complete_drive(drive_id):
    user_id = int(get_jwt_identity())
    admin = SystemUser.query.get(user_id)

    if admin.system_user_role != "admin":
        return jsonify({"msg": "Admin access required"}), 403

    drive = Job.query.get(drive_id)

    if not drive:
        return jsonify({"msg": "Drive not found"}), 404

    drive.closed = True
    db.session.commit()
    return jsonify({"message": "Drive marked as completed"})


@app.route("/admin/applications", methods=["GET"])
@jwt_required()
def get_all_applications():
    user_id = int(get_jwt_identity())
    admin = SystemUser.query.get(user_id)

    if admin.system_user_role != "admin":
        return jsonify({"msg": "Admin access required"}), 403

    applications = Application.query.order_by(Application.apply.desc()).all()
    result = []

    for idx, app in enumerate(applications, 1):
        student = StudentProfile.query.get(app.student_id)
        student_user = SystemUser.query.get(student.user_id) if student else None
        job = Job.query.get(app.job_id)
        company = CompanyProfile.query.get(job.company_id) if job else None
        result.append({
            "sr_no": idx,
            "id": app.id,
            "student_name": student_user.name if student_user
             
              else "Unknown",
            "drive_name": job.title if job else "Unknown",
            "company_name": company.company_name if company 
            else "Unknown",
            "date": app.apply.strftime("%d/%m/%Y") 
            if app.apply else "",
            "status": app.status
        })

    return jsonify(result)


@app.route("/admin/application/<int:app_id>", methods=["GET"])
@jwt_required()
def get_application_details(app_id):
    user_id = int(get_jwt_identity())
    admin = SystemUser.query.get(user_id)

    if admin.system_user_role != "admin":
        return jsonify({"msg": "Admin access required"}), 403

    app = Application.query.get(app_id)

    if not app:
        return jsonify({"msg": "Application not found"}), 404

    student = StudentProfile.query.get(app.student_id)
    student_user = SystemUser.query.get(student.user_id) if student else None
    job = Job.query.get(app.job_id)
    company = CompanyProfile.query.get(job.company_id) if job else None

    return jsonify({
        "student_name": student_user.name 
        if student_user 
        else "Unknown",
        "student_email": student_user.email_address
          if student_user else "",
        "department": student.department if student else "",
        "cgpa": student.cgpa 
        if student else "",
        "skills": student.skills if student else "",
        "resume": student.resume if student else "",
        "drive_name": job.title 
        if job else "",
        "job_title": job.title if job
          else "",
        "company_name": company.company_name if company
          else "",
        "apply_date": app.apply.strftime("%d/%m/%Y") if app.apply else "",
        "status": app.status
    })
#
#
#
#
#
#
#
#

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # agar admin nhi h toh bna do
        existing_admin = SystemUser.query.filter_by(system_user_role="admin").first()

        if not existing_admin:
            admin_db = SystemUser(
                name="admin",
                password="admin",
                email_address="11d@gmail.com",
                system_user_role="admin",
                approve=True
            )
            db.session.add(admin_db)
            db.session.commit()
           

    app.run(debug=True, use_reloader=False, port=5001)