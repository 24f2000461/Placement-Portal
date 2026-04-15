<template>
  <div class="admin-page">
  <button @click="downloadReport" class="download-btn">
    Download Report
  </button>
    <!-- loading screen jab tak data aa raha ho -->
    <div v-if="loading" class="loading-overlay">
     
      <p>Loading...</p>
    </div>

    <!--header sec-->
    <header class="header">
      <div class="header-left">
        
        <div>
          <h1>Admin Dashboard</h1>
          <p class="header-sub">Placement Portal Management</p>
        </div>
      </div>
      <div class="header-right">
        <!-- admin ka naam show karna -->
        <span class="welcome-chip">Welcome, {{ adminName }}</span>

        <!-- search bar company stu drive sab search hoga -->

        <div class="search-wrap">
          <input
            v-model="searchQuery"
            placeholder="Search companies, students, drives..."
            class="search-input"
            @input="handleSearch"
          />
          <span class="search-icon"></span>
        </div>

        <button @click="logout" class="logout-btn">Logout</button>
      </div>
    </header>

    <!-- stats wale cards upar -->
    <div class="stats-row">
      <!-- statCards computed se aa raha hai -->
      <div class="stat-card" v-for="s in statCards" :key="s.label">
        <div class="stat-icon">{{ s.icon }}</div>
        <div class="stat-info">
          <span class="stat-num">{{ s.value }}</span>
          <span class="stat-label">{{ s.label }}</span>
        </div>
      </div>
    </div>

    <!-- main grid - left aur right column -->
    <div class="dashboard-grid">

      <!-- LEFT clm -->
      <div class="left-col">

        <!-- registered copanies ki list -->
        <div class="card">
          <div class="card-header">
            <h2>Registered Companies</h2>
            <!-- filter count badge -->
            
            
          </div>
          <div class="card-body">
            <div v-if="!filteredCompanies.length" class="empty-state">No companies found</div>

            <div v-for="c in filteredCompanies" :key="c.user_id" class="list-item">
              <div class="item-info">
                <span class="item-name">{{ c.company_name }}</span>
                <span class="item-sub">{{ c.email }}</span>
                <!-- industry aur location -->
                <span class="item-meta">{{ c.industry }} · {{ c.location }}</span>
              </div>
              <div class="item-actions">

                <!-- approved h ya pending -->
                <span :class="['status-pill', c.approved ? 'pill-approved' : 'pill-pending']">
                  {{ c.approved ? 'Approved' : 'Pending' }}
                </span>
                <!-- blacklist toggle button -->
                <button
                  @click="toggleBlacklist(c.user_id, c.blacklisted)"
                  :class="['action-btn', c.blacklisted ? 'btn-unblacklist' : 'btn-blacklist']"
                >
                  {{ c.blacklisted ? 'Unblacklist' : 'Blacklist' }}
                </button>
              </div>
            </div>

          </div>
        </div>

        <!-- registered students ki lst -->

        <div class="card">
          <div class="card-header">
            <h2>Registered Students</h2>
           
          </div>
          <div class="card-body">
            <div v-if="!filteredStudents.length" class="empty-state">No students found</div>

            <!-- hr studnt ke liye ek row -->
            <div v-for="s in filteredStudents" :key="s.user_id" class="list-item">
              <div class="item-info">
                <span class="item-name">{{ s.name }}</span>
                <span class="item-sub">{{ s.email }}</span>
                <span class="item-meta">{{ s.department }} {{ s.cgpa ? '· CGPA: ' + s.cgpa : '' }}</span>
              </div>
              <div class="item-actions">
                <button
                  @click="toggleBlacklist(s.user_id, s.blacklisted)"
                  :class="['action-btn', s.blacklisted ? 'btn-unblacklist' : 'btn-blacklist']"
                >
                  {{ s.blacklisted ? 'Unblacklist' : 'Blacklist' }}
                </button>
              </div>
            </div>

          </div>
        </div>

        <!-- pending company approve - jo abhi approve nahi hue -->
        <div class="card">
          <div class="card-header">
            <h2>Company Applications</h2>

            <!-- pending ke liye yellow ab nhi hta diya  -->
            
          </div>
          <div class="card-body">
            <div v-if="!filteredPending.length" class="empty-state">No pending company approvals</div>

            <div v-for="c in filteredPending" :key="c.id" class="list-item">
              <div class="item-info">
                <span class="item-name">{{ c.company_name }}</span>
                <span class="item-sub">{{ c.email }}</span>
                <span class="item-meta">{{ c.industry }} · {{ c.location }}</span>
              </div>
              <!-- approve karne ka butn -->

              <button @click="approveCompany(c.id)" class="action-btn btn-approve">
                 Approve
              </button>
            </div>

          </div>
        </div>

        <!-- pending job approvls -->
        <div class="card">
          <div class="card-header">
            <h2>Pending Job Approvals</h2>
           
          </div>
          <div class="card-body">
            <div v-if="!filteredPendingJobs.length" class="empty-state">No pending job approvals</div>


            <div v-for="job in filteredPendingJobs" :key="job.id" class="list-item">
              <div class="item-info">

                <span class="item-name">
                  {{ job.title }}
                  </span>
                <span class="item-sub">
                  {{ job.company_name }}
                  
                  </span>

                <!-- salary aur date -->
                <span class="item-meta"> {{ job.salary || 'N/A' }} · {{ job.created_at }}</span>
              </div>
              <div class="item-actions">
                <button @click="approveJob(job.id)" class="action-btn btn-approve"> Approve</button>
                <button @click="rejectJob(job.id)" class="action-btn btn-reject"> Reject</button>
              </div>
            </div>

          </div>
        </div>

      </div>
      <!-- left col khtm -->

      <!-- RigHT Col -->
      <div class="right-col">

        <!-- ongoing drive table -->
        <div class="card">

          <div class="card-header">
            <h2>Ongoing Drives</h2>
            
          </div>
          <div class="table-wrap">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Sr No.</th>
                  <th>Drive Name</th>

                  <th>Company</th>
                  <th>Applications</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="!filteredDrives.length">
                  <td colspan="5" class="empty-state">No ongoing drives</td>
                </tr>
                <!-- drives ki list -->

                <tr v-for="drive in filteredDrives" :key="drive.id">
                  <td class="muted">
                    {{ drive.sr_no }}.</td>
                  <td class="bold-cell">{{ drive.drive_name }}</td>
                  <td>{{ drive.company_name }}</td>
                  <td>
                    <!-- application count badge -->

                    <span class="app-count">
                      {{ drive.applications }}

                    </span>
                  </td>
                  <td>
                    <div class="btn-group">
                      <button @click="viewDrive(drive.id)" class="sm-btn btn-view">View</button>
                      <!-- drive complete mark karna -->
                      <button @click="markComplete(drive.id)" class="sm-btn btn-complete">Complete</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- student applicatiotable -->
        <div class="card">
          <div class="card-header">
            <h2>Student Applications</h2>
           
          </div>
          <div class="table-wrap">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Sr No.</th>
                  <th>Name</th>
                  <th>Drive</th>
                  <th>Company</th>
                  <th>Date</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="!filteredApplications.length">
                  <td colspan="7" class="empty-state">No applications found</td>
                </tr>
                <tr v-for="app in filteredApplications" :key="app.id">
                  <td class="muted">{{ app.sr_no }}.</td>
                  <td class="bold-cell">{{ app.student_name }}</td>
                  <td>{{ app.drive_name }}</td>
                  <td>{{ app.company_name }}</td>
                  <td class="muted">{{ app.date }}</td>
                  <td>
                    <!-- status ke hisaab se color change hoga -->
                    <span :class="['status-pill', getStatusClass(app.status)]">{{ app.status }}</span>
                  </td>
                  <td>
                    <button @click="viewApplication(app.id)" class="sm-btn btn-view">View</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>
      <!-- right col khatam -->

    </div>
    <!-- main grid khtam -->


    <!-- ========== DRIVE DETAIL MODAL ========== -->
    <!-- jab View button click ho drive ka -->
    <div v-if="showDriveModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-box">

        <div class="modal-header">
          <h2>{{ driveDetail.drive_name }}</h2>
          <button @click="closeModal" class="close-btn">✕</button>
        </div>

        <div class="modal-body">
          <div class="detail-grid">
            <div class="detail-row">
              <span class="detail-label">Job Title</span>
              <span class="detail-val">{{ driveDetail.job_title }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Company</span>
              <span class="detail-val">{{ driveDetail.company_name }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Salary</span>
              <!-- green color salary ke liye -->
              <span class="detail-val green-val">{{ driveDetail.salary || 'N/A' }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Job Type</span>
              <span class="detail-val">{{ driveDetail.job_type || 'N/A' }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Location</span>
              <span class="detail-val">{{ driveDetail.location }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Deadline</span>
              <!-- deadline red mein dikhana -->
              <span class="detail-val red-val">{{ driveDetail.deadline }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Posted</span>
              <span class="detail-val">{{ driveDetail.posted_date }}</span>
            </div>
          </div>

          <!-- description aur skills full width mein -->
          <div class="detail-row full-width">
            <span class="detail-label">Description</span>
            <p class="detail-desc">{{ driveDetail.description || 'No description provided.' }}</p>
          </div>
          <div class="detail-row full-width">
            <span class="detail-label">Skills Required</span>
            <p class="detail-desc">{{ driveDetail.skills_required || 'Not specified' }}</p>
          </div>
          <div class="detail-row full-width">
            <span class="detail-label">Eligibility</span>
            <p class="detail-desc">{{ driveDetail.eligibility || 'Not specified' }}</p>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="closeModal" class="modal-btn btn-close">Go Back</button>
        </div>

      </div>
    </div>


    <!-- ========== APPLICATION DETAIL MODAL ========== -->
    <!-- jab View click ho application ka -->
    <div v-if="showAppModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-box">

        <div class="modal-header">
          <h2>Student Application</h2>
          <button @click="closeModal" class="close-btn">✕</button>
        </div>

        <div class="modal-body">
          <!-- student ka naam aur basic info upar -->

          <div class="student-app-header">
            <div class="student-avatar">

              <!-- naam ka pehla letter avatar mein -->

              {{ appDetail.student_name ? appDetail.student_name[0].toUpperCase() : 'S' }}
            </div>
            <div>
              <h3>{{ appDetail.student_name }}</h3>
              <p>{{ appDetail.department }}</p>
              <p class="muted-text">{{ appDetail.student_email }}</p>
            </div>
          </div>

          <div class="detail-grid">
            <div class="detail-row">
              <span class="detail-label">Drive</span>
              <span class="detail-val">{{ appDetail.drive_name }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Company</span>
              <span class="detail-val">{{ appDetail.company_name }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">CGPA</span>
              <span class="detail-val">{{ appDetail.cgpa || 'N/A' }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Applied On</span>
              <span class="detail-val">{{ appDetail.apply_date }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Status</span>
              <span :class="['status-pill', getStatusClass(appDetail.status)]">{{ appDetail.status }}</span>
            </div>
          </div>

          <div class="detail-row full-width">
            <span class="detail-label">Skills</span>
            <p class="detail-desc">{{ appDetail.skills || 'Not mentioned' }}</p>
          </div>
        </div>

        <div class="modal-footer">
          <!-- resume link agar hai to -->
          <a v-if="appDetail.resume" :href="appDetail.resume" target="_blank" class="modal-btn btn-resume">📄 View Resume</a>
          <button @click="closeModal" class="modal-btn btn-close">Go Back</button>
        </div>

      </div>
    </div>

  </div>
</template>

<script>
// api service import kar raha hoon

import api from "@/services/api";

export default {
  name: "AdminDashboard",

  data() {
    return {
      loading: false,
      adminName: "Admin",    // baad mein localStorage se set hoga
      searchQuery: "",       // search input

      // stats default values
      stats: {
        total_companies: 0,
        total_students: 0,
        total_drives: 0,
        total_applications: 0,
        total_pending_jobs: 0
      },

      // data arrays
      companies: [],
      students: [],
      pendingCompanies: [],
      pendingJobs: [],
      drives: [],
      applications: [],

      // modal ke liye flags
      showDriveModal: false,
      driveDetail: {},        // selected drive ka data
      showAppModal: false,
      appDetail: {},          // selected application ka data
    };
  },

  computed: {
    // stats cards array banana
    statCards() {
      return [
        { icon: "", label: "Companies",     value: this.stats.total_companies },
        { icon: "", label: "Students",      value: this.stats.total_students },
        { icon: "", label: "Ongoing Drives",value: this.stats.total_drives },
        { icon: "", label: "Applications",  value: this.stats.total_applications },
        { icon: "", label: "Pending Jobs",  value: this.stats.total_pending_jobs },
      ];
    },

    // search query lowercase mein
    q() {
      return this.searchQuery.toLowerCase().trim();
    },

    // company filter with search
    filteredCompanies() {
      if (!this.q) return this.companies;
      return this.companies.filter(c =>
        c.company_name?.toLowerCase().includes(this.q) ||
        c.email?.toLowerCase().includes(this.q) ||
        c.industry?.toLowerCase().includes(this.q)
      );
    },

    // student filter
    filteredStudents() {
      if (!this.q) return this.students;
      return this.students.filter(s =>
        s.name?.toLowerCase().includes(this.q) ||
        s.email?.toLowerCase().includes(this.q) ||
        s.department?.toLowerCase().includes(this.q)
      );
    },

    // pending companies filter

    filteredPending() {
      if (!this.q) return this.pendingCompanies;
      return this.pendingCompanies.filter(c =>
        c.company_name?.toLowerCase().includes(this.q) ||
        c.email?.toLowerCase().includes(this.q)
      );
    },

    // pending jobs filter

    filteredPendingJobs() {
      if (!this.q) return this.pendingJobs;
      return this.pendingJobs.filter(j =>
        j.title?.toLowerCase().includes(this.q) ||
        j.company_name?.toLowerCase().includes(this.q)
      );
    },

    // ongoing drives filter
    filteredDrives() {
      if (!this.q) return this.drives;
      return this.drives.filter(d =>
        d.drive_name?.toLowerCase().includes(this.q) ||
        d.company_name?.toLowerCase().includes(this.q)
      );
    },

    // application filter
    filteredApplications() {
      if (!this.q) return this.applications;
      return this.applications.filter(a =>
        a.student_name?.toLowerCase().includes(this.q) ||
        a.drive_name?.toLowerCase().includes(this.q) ||
        a.company_name?.toLowerCase().includes(this.q)
      );
    },
  },

  async mounted() {
    // check karo token hai ya nahi

    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");

    if (!token || role !== "admin") {

      // agar admin   nahi hai to login pe bejo

      this.$router.push("/login");
      return;
    }

    // admin ka naam set karo
    this.adminName = localStorage.getItem("userName") || "Admin";

    // sab data load karo
    await this.loadAll();
  },

  methods: {

    // // ek baar mein sab data le raha, nahi to loading bar baar baar aayega
    async loadAll() {
      this.loading = true;
      try {
        // sab APIs parallel mein call ho rahi hain
        const [statsRes, companiesRes, studentsRes, pendingRes, pendingJobsRes, drivesRes, appsRes] = await Promise.all([
          api.get("/admin/stats"),

          api.get("/admin/companies"),
          api.get("/admin/students"),
          api.get("/admin/pending-companies"),

          api.get("/admin/pending-jobs"),
          api.get("/admin/ongoing-drives"),
          api.get("/admin/applications"),

        ]);

        // response data set karo
        this.stats            = statsRes.data;

        this.companies        = companiesRes.data;
        this.students         = studentsRes.data;
        this.pendingCompanies = pendingRes.data;

        this.pendingJobs      = pendingJobsRes.data;
        this.drives           = drivesRes.data;

        this.applications     = appsRes.data;

      } catch (e) {
        // error log karo
        console.error("Load error:", e);
      } finally {
        this.loading = false;

      }
    },
async downloadReport() {
  try {
    this.loading = true;
    const res = await api.get("/admin/generate-report");
    const taskId = res.data.task_id;
    let finished = false;

    while (!finished) {
      await new Promise(r => setTimeout(r, 2000));
      const statusRes = await api.get(`/admin/report-status/${taskId}`);

      if (statusRes.data.status === "done") {
        window.open("http://localhost:5001" + statusRes.data.download_url, "_blank");
        finished = true;
      }
      if (statusRes.data.status === "failed") {
        alert("Report generation failed");
        break;
      }
    }
  } catch (err) {
    console.error(err);
    alert("Error downloading report");
  } finally {
    this.loading = false;
  }
},
    // search computed property handle kar raha hai isliye yahan kuch nahi
    handleSearch() {

      // computed property automatically filter karti hai
    },

    // company approve karna
    async approveCompany(userId) {
      try {
        await api.post(`/admin/approve-company/${userId}`);

        // approve ke baad data refresh karo
        await this.loadAll();
      } catch (e) {
        alert(e.response?.data?.msg || "Error");

      }
    },

    // blacklist ya unblacklist karna
    async toggleBlacklist(userId, currentStatus) {

      var action = currentStatus ? "unblacklist" : "blacklist"; 
      // var use kiya yahan galti se
      if (!confirm(`Are you sure you want to ${action} this user?`)) return;
      try {

        await api.post(`/admin/toggle-blacklist/${userId}`);
        await this.loadAll();

      } catch (e) {
        alert(e.response?.data?.msg || "Error");

      }
    },

    // job approve karna
    async approveJob(jobId) {

      try {
        await api.post(`/admin/approve-job/${jobId}`);

        await this.loadAll();
      } catch (e) {
        alert(e.response?.data?.msg || "Error");
      }
    },

    // job reject aur delete karna
    async rejectJob(jobId) {
      if (!confirm("Reject and delete this job posting?")) return;

      try {
        await api.delete(`/admin/reject-job/${jobId}`);
        await this.loadAll();
      } catch (e) {

        alert(e.response?.data?.msg || "Error");
      }
    },

    // drive complete mark karna
    async markComplete(driveId) {

      if (!confirm("Mark this drive as complete?")) return;
      try {
        await api.post(`/admin/complete-drive/${driveId}`);
        await this.loadAll();
      } catch (e) {

        alert(e.response?.data?.msg || "Error");
      }
    },

    // drive ka detail modal kholna
    async viewDrive(driveId) {
      try {
        const res = await api.get(`/admin/drive/${driveId}`);
        this.driveDetail    = res.data;     // extra space yaha - minor style inconsitency
        this.showDriveModal = true;

      } catch (e) {
        alert("Could not load drive details");
      }
    },

    // application ka detal modal kholna
    async viewApplication(appId) {
      try {
        const res = await api.get(`/admin/application/${appId}`);
        this.appDetail   = res.data;
        this.showAppModal = true;
      } catch (e) {
        alert("Could not load application details");
      }
    },

    // dono modals band karna
    closeModal() {
      this.showDriveModal = false;

      this.showAppModal   = false;
    },

    // status ke hisaab se CSS class return karna
    getStatusClass(status) {
      if (!status) return "";
      const s = status.toLowerCase();
      if (s === "shortlisted")             
      
      return "pill-approved";
      if (s === "rejected")                
       return "pill-rejected";
      if (s === "applied" || s === "pending")

       return "pill-pending";

      if (s === "waitlisted")              
       return "pill-waitlisted";
      return "pill-pending"; // default hoga 
    


    },

    // logout fuction
    logout() {
      localStorage.clear();
      this.$router.push("/login");
    },

  } // methods khatam

}; // export khatam
</script>

<style scoped>
* { box-sizing: border-box; 
margin: 0;

padding: 0; }

/* main page background */
.admin-page {
  min-height: 100vh;
  background: #f1f5f9;
  font-family: 'Inter', -apple-system, sans-serif;
  padding-bottom: 40px;
}

/* loading overlay */
.loading-overlay {
  position: fixed; inset: 0;
  background: rgba(255, 255, 255, 0.88);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  gap: 16px
}

/* spinner animation  ab nhi kr rhi ye m*/


/* HEADER  */
.header {
  background: linear-gradient(135deg, #1e293b, #0f172a);
  padding: 18px 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
}

.header-left { display: flex; align-items: center; gap: 14px; }

.logo {
  width: 44px; height: 44px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px;
}

.header-left h1 { font-size: 20px; 
font-weight: 700; 
color: white; }


.header-sub     { font-size: 12px; 
color: #64748b; }

.header-right { display: flex;
 align-items: center; 
 gap: 12px; 
 flex-wrap: wrap; }

.welcome-chip {
  background: rgba(255, 255, 255, 0.1);
  color: #cbd5e1;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
}

/* search bar stylng */

.search-wrap { position: relative; 
display: flex;
 align-items: center; }

.search-input {
  padding: 9px 16px 9px 36px;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.15);

  background: rgba(255, 255, 255, 0.08);

  color: white;
  font-size: 13px;
  width: 260px;
  outline: none;
  transition: all 0.2s;
}
.search-input::placeholder { color: #64748b; }
.search-input:focus {

  background: rgba(255, 255, 255, 0.14);
  border-color: #3b82f6;
  width: 300px;
}

.search-icon { position: absolute; 
left: 12px; font-size: 14px }

/* logout button */
.logout-btn {
  padding: 8px 18px;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.logout-btn:hover { background: #b91c1c; }

/*STAT ROW */
.stats-row {
  display: flex;
  gap: 16px;
  padding: 24px 40px 0;
  overflow-x: auto;
}

.stat-card {
  flex: 1;
  min-width: 160px;
  background: white;
  border-radius: 14px;
  padding: 20px 22px;
  display: flex;
  align-items: center;
  gap: 14px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  border: 1px solid #e2e8f0;
  transition: transform 0.2s;
}
.stat-card:hover { transform: translateY(-2px); 
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); 
}

.stat-icon { font-size: 28px
 }

.stat-num {
  display: block;
  font-size: 28px;
  font-weight: 800;
  color: #1e293b;
  line-height: 1;
}
.stat-label { font-size: 12px;
 color: #64748b;
  font-weight: 500 }

/* MAIN GRID */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1.4fr;
  gap: 20px;
  padding: 20px 40px 0;
}

.left-col, .right-col { display: flex; flex-direction: column; gap: 20px; }

/*CARD  */
.card {
  background: white;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}

.card-header {
  padding: 16px 20px;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  align-items: center;
  gap: 10px;
}
.card-header h2 { font-size: 15px;
 font-weight: 700; 
 color: #0f172a; }

/* badge ye remove kr diya mene ab */

/* list item styling */

.list-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  border-bottom: 1px solid #f8fafc;
  gap: 10px;
  transition: background 0.15s;
}
.list-item:hover      { background: #f8fafc; }
.list-item:last-child { border-bottom: none; }

.item-info { 
  display: flex; 
  flex-direction: column; 
  gap: 2px; flex: 1; }
.item-name { font-size: 14px;
 font-weight: 600; 
 color: #1e293b; }

.item-sub  { font-size: 12px; 
color: #64748b; }
.item-meta { font-size: 11px; 
color: #94a3b8; }

.item-actions { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }

/*ACTION BUTTON */
.action-btn {
  padding: 6px 14px;
  border: none;
  border-radius: 7px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}

/* blacklist btn clors */
.btn-blacklist   { background: #fef2f2; 

color: #dc2626; }
.btn-blacklist:hover { background: #dc2626;

color: white; }

.btn-unblacklist { background: #f0fdf4; 
color: #16a34a; }
.btn-unblacklist:hover { background: #16a34a; 
color: white; }

.btn-approve { background: #f0fdf4; 
color: #16a34a; }

.btn-approve:hover { background: #16a34a; 
color: white; }

.btn-reject { background: #fef2f2; 
color: #dc2626; }

.btn-reject:hover { background: #dc2626;
 color: white }

/* STATUS PILLS */
.status-pill {
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  white-space: nowrap;
}

/* alag alag status ke liye colors */
.pill-approved  { background: #f0fdf4; 
color: #16a34a;
 border: 1px solid #bbf7d0; }
.pill-pending   { background: #fffbeb;
 color: #d97706; 
 border: 1px solid #fde68a; }

.pill-rejected  { background: #fef2f2;
 color: #dc2626; 
 border: 1px solid #fecaca; }


.pill-waitlisted{ background: #eff6ff;
 color: #3b82f6; 
 border: 1px solid #bfdbfe }

/*  dATA TABlE*/
.table-wrap { overflow-x: auto; }

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.data-table th {
  background: #1e293b;
  color: #94a3b8;
  padding: 12px 16px;
  text-align: left;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
}

.data-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #f1f5f9;
  color: #374151;
  vertical-align: middle;
}

.data-table tr:hover td   { background: #f8fafc; }
.data-table tr:last-child td { border-bottom: none; }

/* text helper... */
.muted     { color: #94a3b8; }
.bold-cell { font-weight: 600; color: #1e293b; }

.app-count {
  background: #eff6ff;
  color: #3b82f6;
  border-radius: 20px;
  padding: 2px 10px;
  font-size: 12px;
  font-weight: 700;
}

.btn-group { display: flex; gap: 6px; }

/* small butntable ke andar -->*/
.sm-btn {
  padding: 5px 11px;
  border: none;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}

.btn-view { background: #eff6ff;
 color: #3b82f6; }

.btn-view:hover { background: #3b82f6; 

color: white; }

.btn-complete {
   background: #f0fdf4; 
   color: #16a34a; }

.btn-complete:hover { 
  background: #16a34a; 
  color: white
  
  }

/* empty state msg */


.empty-state {
  text-align: center;
  padding: 28px;
  color: #94a3b8;
  font-size: 13px;
  font-style: italic;
}

/*  MOdal*/
.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(15, 23, 42, 0.55);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-box {
  background: white;
  border-radius: 20px;
  width: 100%;
  max-width: 540px;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.modal-header h2
 { font-size: 18px;
  font-weight: 700; 
  color: #0f172a
  
  }

/* close button */

.close-btn {
  background: #f1f5f9;
  border: none;
  border-radius: 8px;
  width: 32px; height: 32px;
  cursor: pointer;
  font-size: 14px;
  color: #64748b;
  transition: all 0.15s;
}
.close-btn:hover { background: #e2e8f0; color: #1e293b; }

.modal-body { padding: 20px 24px; }

/* 2 col grid modal ke andar */

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-bottom: 16px;
}

.detail-row { display: flex;
 flex-direction: column;
  gap: 4px
   }

/* full width row - skills desc wgera  etc */


.full-width { grid-column: 1 / -1; 
margin-top: 8px;

}

.detail-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;

  letter-spacing: 0.07em;
  color: #94a3b8;
}
.detail-val { font-size: 14px; 
font-weight: 600; 

color: #1e293b

}

.detail-desc {
  font-size: 13px;
  color: #64748b;
  line-height: 1.65;
  background: #f8fafc;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

/* color helper */
.green-val { 
  color: #16a34a; }
.red-val   { 
  
  color: #dc2626; }

/* stu. heder in applicatin modal */
.student-app-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f1f5f9;
}

/* avatar circle */
.student-avatar {
  width: 52px; height: 52px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  color: white;
  font-size: 22px;
  font-weight: 700;
  border-radius: 50%;
  display: flex; 
  
  align-items: center; 
  justify-content: center;
  flex-shrink: 0;
}

.student-app-header h3 
{ font-size: 16px; 

font-weight: 700; 
color: #1e293b; 
}
.student-app-header p  {
   font-size: 13px; 
   color: #64748b; margin-top: 2px }

.muted-text { color: #94a3b8 !important;
 font-size: 12px !important; }

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid #f1f5f9;

  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* modal buttons */
.modal-btn {
  padding: 9px 18px;
  border: none;

  border-radius: 9px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  text-decoration: none;

  display: inline-flex;

  align-items: center;
}

.btn-close  {
   background: #f1f5f9;
    color: #374151; }

.btn-close:hover {
   background: #e2e8f0 }

.btn-resume { 
  background: #3b82f6;

   color: white; }

.btn-resume:hover { 
background: #2563eb }



</style>