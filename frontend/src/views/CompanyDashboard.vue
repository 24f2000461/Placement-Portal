<template>
  <div class="main-page">

    <!-- loader show hoga jab data ftch ho rha ho -->

    <div v-if="isLoading" class="loader">


      
    </div>

    <header class="header">
<button @click="downloadCompanyReport" class="btn btn-green">
  Download Report
</button>
      <div class="header-left">


        <!-- company ka pehla letter show krega logo ki jagah -->
        <div class="logo-box">{{ firstLetter }}</div>


        <div>
          <h1>{{ companyName || 'Welcome' }}</h1>
          <p class="header-sub">
            {{ companyDetails.industry }}

            <span v-if="companyDetails.location"> · {{ companyDetails.location }}</span>
          </p>
        </div>
      </div>
      <div class="header-right">
        <button @click="goToCreateJob" class="btn btn-blue">+ Create Drive</button>
        <button @click="toggleProfileForm" class="btn btn-outline">


          <!-- agar profile bani h to Edit dikhao warna Setup kr lo -->

          {{ showForm ? 'Close Profile' : (profileExists ? 'Edit Profile' : 'Setup Profile') }}
        </button>
        <button @click="logout" class="btn btn-danger">Logout</button>
      </div>
    </header>

    <!-- stat sirf tab dikhnge jab data aaye -->
    <div class="stats-row" v-if="dashStats">
      <div class="stat-card">

        <span class="stat-num">{{ dashStats.total_jobs }}</span>
        <span class="stat-label">Total Drives</span>
      </div>
      <div class="stat-card">

        <span class="stat-num">{{ dashStats.total_applications }}</span>
        <span class="stat-label">Applications</span>

      </div>
      <div class="stat-card">
        <span class="stat-num">{{ dashStats.shortlisted }}</span>

        <span class="stat-label">Shortlisted</span>
      </div>
    </div>

    <!-- pro form toggle hoga is div se -->
    <div v-if="showForm" class="profile-card">


      <h3>{{ profileExists ? 'Edit Company Profile' : 'Create Company Profile' }}</h3>
      <div class="profile-grid">

        <div class="form-group">
          <label>Company Name *</label>

          <input v-model="profileData.company_name" placeholder="e.g. TechCorp Pvt Ltd" />
        </div>
        <div class="form-group">
          <label>Industry *</label>

          <input v-model="profileData.industry" placeholder="e.g. Information Technology" />
        </div>
        <div class="form-group">
          <label>Website</label>
          <input v-model="profileData.website" placeholder="https://yourcompany.com" />
        </div>
        <div class="form-group">
          <label>Location *</label>
          <input v-model="profileData.location" placeholder="e.g. Bangalore, India" />
        </div>
        <div class="form-group">
          <label>Company Size</label>

          <select v-model="profileData.comp_size">
            <option value="">Select size</option>

            <option value="1-50">1-50 employees</option>

            <option value="51-200">51-200 employees</option>
            <option value="201-500">201-500 employees</option>
            <option value="500+">500+ employees</option>
          </select>
        </div>
      </div>
      <div class="form-group full-width">
        <label>Company Description</label>


        <textarea v-model="profileData.des" placeholder="Describe your company, culture, vision..."></textarea>
      </div>


      <!-- succes ya err msg yaha aayega -->

      <div v-if="formMsg" :class="['msg-box', formMsgType]">{{ formMsg }}</div>
      <button @click="submitProfile" :disabled="savingProfile" class="btn btn-green">

        {{ savingProfile ? 'Saving...' : (profileExists ? 'Update Profile' : 'Create Profile') }}
      </button>
    </div>


    <div class="dashboard-content">

      <!-- upcomig drives wala section -->
      <div class="section-card">
        <div class="section-head">

          <h2>Upcoming Drives</h2>
         
        </div>
        <div class="table-wrap">
          <table class="data-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Drive Name</th>
                <th>Type</th>
                <th>Salary</th>
                <th>Deadline</th>

                <th>Status</th>
                <th>Applications</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <!-- agar koi drive nhi h to ye msg dikhega -->

              <tr v-if="!activeDrives.length">
                <td colspan="8" class="empty">No upcoming drives. Create one!</td>
              </tr>
              <tr v-for="(drive, i) in activeDrives" :key="drive.id">
                <td class="muted">{{ i + 1 }}.</td>
                <td class="drive-name">{{ drive.title }}</td>
                <td class="muted">{{ drive.job_type }}</td>

                <td class="salary-text">{{ drive.salary }}</td>

                <td class="muted">{{ drive.deadline }}</td>
                <td>
                  <!-- aprove h to green  warna yellow -->

                  <span :class="['status-pill', drive.approve ? 'pill-approved' : 'pill-pending']">
                    {{ drive.approve ? 'Approved' : 'Pending' }}
                  </span>

                </td>
                <td>

                  <span class="app-badge">{{ drive.applications_count }}</span>
                </td>
                <td>

                  <div class="btn-row">
                    
                    <!-- view applications ka btn sirf approve drive pe dikhega -->
                    <button

                      v-if="drive.approve"
                      @click="viewApplications(drive)"
                      class="sm-btn btn-view"

                    >View Applications</button>

                    <button @click="markComplete(drive.id)" class="sm-btn btn-complete">
                      Mark Complete
                    </button>
                  </div>

                </td>
              </tr>

            </tbody>


          </table>
        </div>

      </div>

      <!-- close ya complete drives -->
      <div class="section-card">
        <div class="section-head">

          <h2>Closed Drives</h2>
        
        </div>
        <div class="table-wrap">
          <table class="data-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Drive Name</th>
                <th>Type</th>

                <th>Salary</th>
                <th>Date</th>

                <th>Total Applications</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="!doneDrives.length">
                <td colspan="6" class="empty">No closed drives yet</td>
              </tr>
              <tr v-for="(drive, i) in doneDrives" :key="drive.id">
                <td class="muted">{{ i + 1 }}.</td>

                <td class="drive-name">{{ drive.title }}</td>
                <td class="muted">{{ drive.job_type }}</td>
                <td class="salary-text">{{ drive.salary }}</td>

                <td class="muted">{{ drive.created_at }}</td>
                <td><span class="app-badge">{{ drive.applications_count }}</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- applicatons modal - click outside karo to close -->

    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal-box large-modal">

        <div class="modal-header">
          <div>
            <h2>Applications — {{ selectedTitle }}</h2>
            <p class="modal-sub">Review and update application statuses</p>

          </div>

          <button @click="showModal = false" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div v-if="!appList.length" class="empty">No applications received yet</div>
          <!-- har application ka card -->
          <div v-for="app in appList" :key="app.id" class="app-card">
            <div class="app-avatar">{{ app.student_name[0] }}</div>


            <div class="app-info">
              <div class="app-name">{{ app.student_name }}</div>

              <div class="app-meta">
                {{ app.department }}
                <span v-if="app.cgpa"> · CGPA: {{ app.cgpa }}</span>
              </div>
              <div class="app-skills">{{ app.skills }}</div>
            </div>
            <div class="app-actions">
              <span :class="['status-pill', getStatusClass(app.status)]">{{ app.status }}</span>
              <!-- status change karne ka dropdown -->
              <select v-model="app.newStatus" class="status-select">

                <option value="">Change Status</option>
                <option value="Shortlisted">Shortlist</option>

                <option value="Waitlisted">Waitlist</option>
                <option value="Rejected">Reject</option>
              </select>
              <!-- save butn disable rahega jab tak koi option select na ho -->
              <button @click="updateStatus(app)" :disabled="!app.newStatus" class="sm-btn btn-save">
                Save
              </button>
              <a v-if="app.resume" :href="app.resume" target="_blank" class="sm-btn btn-resume">
                Resume
              </a>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showModal = false" class="btn btn-outline">Close</button>
        </div>
      </div>
    </div>

  </div>

</template>

<script>
import api from "@/services/api";

export default {
  name: "CompanyDashboard",

  data() {
    return {
      isLoading: false,
      companyName: "",
      companyDetails: { industry: "", location: "" },
      firstLetter: "C",
      profileExists: false,
      showForm: false,

      // profile form ka data

      profileData: 
      {
        company_name: "",
        industry: "",
        website: "",
        location: "",
        comp_size: "",
        des: "",
      },
      formMsg: "",
      formMsgType: "success-box",
      savingProfile: false,

      dashStats: null,
      activeDrives: [],
      doneDrives: [],


      //   modal related state
      showModal: false,

      selectedDriveId: null,
      selectedTitle: "",

      appList: [],
    };
  },

  async mounted() {
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");

    //  agar token nahi   h ya role company nahi h to login pe bhejo
    if (!token || role !== "company") {
      this.$router.push("/login");
      return;
    }

    await this.loadData();
  },

  methods: {
    async loadData() {
      this.isLoading = true;

      try {
        const profileRes = await api.get("/company/profile");
        const p = profileRes.data;

        this.profileExists = p.has_profile;

        // yaha check kar raha hu ki name empty to nahi

        this.companyName = p.company_name || localStorage.getItem("userName") || "";


        this.firstLetter = this.companyName ? this.companyName[0].toUpperCase() : "C";
        this.companyDetails = {
          industry: p.industry || "",

          location: p.location || "",
        };

        //   agar profile alredy bani h to form mein prefill karo
        if (p.has_profile) {
          this.profileData = { ...this.profileData, ...p };

        }

        
        // yaha parallel API call kar raha hu taaki load fast ho
// warna ek ke baad ek karne pe slow lagta
        const [jobsRes, statsRes] = await Promise.all([
          api.get("/company/jobs"),
          api.get("/company/dashboard_stats"),
        ]);

        const jobs = jobsRes.data.jobs || [];


        if (!this.companyName && jobsRes.data.company_name) 
        {
          this.companyName = jobsRes.data.company_name;

          this.firstLetter = this.companyName[0]?.toUpperCase() || "C";
        }

        // clos or upcoming drives alag karo


        this.activeDrives = jobs.filter(j => !j.closed);

// closed drives alag store kar raha hu
        this.doneDrives = jobs.filter(j => j.closed);

        this.dashStats = statsRes.data;

      } catch (err) {
        console.error("Failed to load dashboard:", err);
      } finally {
        this.isLoading = false;
      }
    },

    toggleProfileForm() {
      this.showForm = !this.showForm;

      this.formMsg = "";      //   messag clear karo jab form toggle ho
    },

    async submitProfile() {
      const { company_name, industry, location } = this.profileData;

      // requred field check
      if (!company_name || !industry || !location) {

        this.formMsg = "Company Name, Industry and Location are required";
        this.formMsgType = "error-box";
        return;

      }

      this.savingProfile = true;
      this.formMsg = "";

      try {

        await api.post("/company_dashboard/company_profile", this.profileData);

        this.profileExists = true;

        this.companyName = company_name;
        this.firstLetter = company_name[0].toUpperCase();

        this.companyDetails = { industry, location };

        this.formMsg = this.profileExists ? "Profile updated!" : "Profile created!";

        this.formMsgType = "success-box";

        // thodi der baad form band kar do
        setTimeout(() => {
          this.showForm = false;
          this.formMsg = "";
        }, 1500);

      } catch (err) {
        this.formMsg =
          err.response?.data?.msg ||
          err.response?.data?.message ||

          "Something went wrong. Try again.";
        this.formMsgType = "error-box";
      } finally {
        this.savingProfile = false;
      }
    },

    goToCreateJob() {
      // pehle profile check karo
      if (!this.profileExists) {

        alert("Please set up your company profile before posting a drive.");
        this.showForm = true;

        return;
      }

      this.$router.push("/create-job");

    },

    async markComplete(driveId) {
      const confirmed = confirm(
        "Mark this drive as complete? It will move to Closed Drives."
      );
      if (!confirmed) return;

      try {
        await api.post(`/company/drive/${driveId}/complete`);
        await this.loadData(); // data refresh karo
      } catch (err) {
        alert(err.response?.data?.msg || "Drive complete nahi ho paya.");
      }
    },

    async viewApplications(drive) {
      this.selectedDriveId = drive.id;
      this.selectedTitle = drive.title;
      this.showModal = true;
      this.appList = []; // pehle clear karo

      try {
        const res = await api.get(`/company/drive/${drive.id}/applications`);
        
        // newStatus field add karo har application mein status change ke liye
        this.appList = (res.data.applications || []).map(a => ({
          ...a,

          newStatus: "",
        }));
      } catch {
        alert("Could not load applications. Please try again.");
        this.showModal = false;
      }
    },

    async updateStatus(app) {
      if (!app.newStatus) return;

      try {
        await api.post(`/company/application/${app.id}/status`, {
          status: app.newStatus,
        });
        // locally bhi update karo dobara fetch nahi karna
        app.status = app.newStatus;
        app.newStatus = "";
      } catch (err) {
        alert(err.response?.data?.msg || "Status update failed.");
      }
    },
async downloadCompanyReport() {
  try {
    const res = await api.get("/company/generate-report");
    const taskId = res.data.task_id;
    let done = false;

    while (!done) {
      await new Promise(r => setTimeout(r, 2000));

      // FIX 1: was /admin/report-status — company user gets 403 there
      const statusRes = await api.get(`/company/report-status/${taskId}`);

      // FIX 2: was checking .status === "done" but backend was returning .state
      if (statusRes.data.status === "done") {
        const url = statusRes.data.download_url;
        window.open("http://localhost:5001" + url, "_blank");
        done = true;
      }

      if (statusRes.data.status === "failed") {
        alert("Report generation failed");
        break;
      }
    }

  } catch (err) {
    console.error(err);
    alert("Error downloading report");
  }
},
    // status ke hisaab se CSS class return karo
    getStatusClass(status) {

      if (!status) return "";

      switch (status.toLowerCase()
      ) {

        case "shortlisted": return "pill-approved";
        case "rejected":    return "pill-rejected";
        case "waitlisted":  return "pill-waitlisted";
        default:            return "pill-pending";
      }
    },

    logout() {
      localStorage.clear();
      this.$router.push("/login");
    },
  },
};

</script>

<style scoped>
* { box-sizing: border-box; 

margin: 0;

 padding: 0
 
 }

/* main  poora page cover krega */
.main-page {
  min-height: 100vh;
  background: #0f172a;
  font-family: 'Inter', -apple-system, sans-serif;
  color: white;
  padding-bottom: 40px;
}

/* ye loader fetch ke time screen pe aayega */
.loader {
  position: fixed; inset: 0;
  background: rgba(15, 23, 42, 0.7);
  display: flex; align-items: center; 
  
  justify-content: center;
  z-index: 9999;
}

/* ye thoda adjust karna padega baad me */
.header {
  background: #1e293b;
  border-bottom: 1px solid #334155;
  padding: 18px 40px; /* maybe reduce padding later */
  display: flex;


  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap  
  
  /* chhoti screen pe wrap ho jaye */
}
/*header lft ka stule h ye */
.header-left { 
  display: flex; 

align-items: center; 
gap: 14px; }

/* company name ka pehla letter yahan dikhega */
.logo-box {
  width: 46px; height: 46px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  color: white; 
  font-size: 20px;
  
  font-weight: 800;
  border-radius: 12px;

  display: flex; 
  align-items: center; 
  
  justify-content: center;
}

.header-left h1 

{ font-size: 20px;
 font-weight: 700; 
 }
.header-sub { 
  font-size: 12px;
   color: #64748b;    /* grey rakhna hai ye */
   
   margin-top: 2px; 
   
   }


.header-right{
  display: flex;

 align-items:
  center; gap: 10px; 
  }

/* stats wali row - 3 cards side by side */

.stats-row {
  display: flex;
  gap: 16px;
  padding: 24px 40px;
}
.stat-card {
  flex: 1;
  background: #1e293b;
  border: 1px solid #334155;

  border-radius: 14px;
  padding: 20px 24px;
  display: flex;
   flex-direction: 
   column; gap: 4px;
}
/* bada no. */
.stat-num
 { font-size: 32px; 
 font-weight: 800; 
 color: #60a5fa;
  }
.stat-label {
   font-size: 12px; 
   color: #64748b;
   font-weight: 500
    }

/* profile setupyaedit form ka card */
.profile-card {
  margin: 0 40px 24px;
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 16px;
  padding: 28px;
}

.profile-card h3 {
   font-size: 16px; 

   font-weight: 700; 
   margin-bottom: 20px; 
   
   color: #e2e8f0; }

/* 2 col grid form ke liye */
.profile-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}
.form-group { display: flex;
 flex-direction: column; 
 
 gap: 6px; }

/* desc wala full width lega */
.full-width 
{ grid-column: 1 / -1; }
.form-group label {
  font-size: 11px; font-weight: 700;
  text-transform: uppercase; 
  
  letter-spacing: 0.05em;
  color: #64748b
}
/* input slt textarea sab ka common style */
.form-group input,
.form-group select,

.form-group textarea {
  padding: 10px 14px;
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 8px;
  color: white; font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
 
}
/* focus pe blue border*/
.form-group input:focus,
.form-group select:focus,

.form-group textarea:focus { 
  
  border-color: #3b82f6; }


.form-group textarea {
  
  resize: vertical; 
min-height: 80px;
 font-family: inherit; }

.dashboard-content {
  padding: 0 40px;
  display: flex; flex-direction: column; gap: 24px;
}

/* section card - drives ke liye*/
.section-card {
  background: #1e293b;
  border: 1px solid #334155;

  border-radius: 16px;
  overflow: hidden;

}
.section-head {
  padding: 16px 22px;
  border-bottom: 1px solid #334155;
  display: flex; align-items: center; gap: 10px;
}
.section-head h2 {
   font-size: 15px;
 font-weight: 700;
  color: #e2e8f0; }

/*count badge  upcoming ko blur  ye ab nhi chiye extra h */
.badge {
  background: #3b82f6; color: white;
  border-radius: 20px; padding: 2px 9px;
  font-size: 11px; font-weight: 700;
}
/* closed ka grey 

 */


.table-wrap { 
  overflow-x: auto;

}
.data-table { width: 100%; 
border-collapse: collapse;

font-size: 13px; }

.data-table th {
  background: #0f172a; color: #64748b;

  padding: 12px 16px; text-align: left;
  font-size: 11px;
  
  font-weight: 600;


  text-transform: uppercase; 
  
  letter-spacing: 0.05em;
  white-space: nowrap
}
.data-table td {
  padding: 13px 16px;

  border-bottom: 1px solid #334155;
  color: #cbd5e1; vertical-align: middle;
}
.data-table tr:last-child td { border-bottom: none; }
/* row hover pe halka highlght */

.data-table tr:hover td 
{ 
  
  background: rgba(59, 130, 246, 0.04); 

}

.muted { color: #64748b; }
.drive-name { font-weight: 600; color: #e2e8f0; }

/* salary green dikhgi */
.salary-text { color: #22c55e; font-weight: 600; }

/* applications count pill */
.app-badge {
  background: #1d4ed8; color: #bfdbfe;
  border-radius: 20px;
   padding: 2px 10px;
  font-size: 12px;
  
  font-weight: 700;
}
/* empty state mesg */
.empty {
  text-align: center;
  
  padding: 32px;
  color: #475569; 
  
  font-style: italic;
}

/*status approved

pending rejecte etc */
.status-pill {

  padding: 3px 10px; border-radius: 20px;

  font-size: 11px; font-weight: 700;
  
  white-space: nowrap;
}

.pill-approved  { background: #052e16; 
color: #86efac; }
.pill-pending 
  { background: #422006;

color: #fde68a; }
.pill-rejected  { background: #450a0a;
 color: #fca5a5; }

.pill-waitlisted


 { background: #1e3a5f;
 color: #93c5fd }

/* common   button styles */
.btn {
  padding: 9px 18px; border-radius: 8px; border: none;
  font-size: 13px; font-weight: 600; cursor: pointer;
  transition: all 0.2s; white-space: nowrap;
}
.btn-blue  { 
  background: #2563eb; 
  
  color: white; }

.btn-blue:hover { background: #1d4ed8; 


}



.btn-outline  {
   background: transparent; 
border: 1px solid #60a5fa;


 color: #60a5fa
 
 }

.btn-outline:hover {
  
  background: rgba(96, 165, 250, 0.1);
  
  }

.btn-danger  
 { 
  
  background: #dc2626; 
color: white; 

}
.btn-danger:hover { background: #b91c1c

}
.btn-green  { background: #16a34a; 

color: white; 

}
.btn-green:hover {
  
  background: #15803d; }
.btn:disabled 

{ opacity: 0.5;
 cursor: not-allowed; }

.btn-row { display: flex;
 gap: 6px; }

/* table ke andar chote action btns */
.sm-btn {
  padding: 5px 11px; border: 
  none; border-radius: 6px;
  font-size: 11px; 

  font-weight: 600; cursor: pointer;
  transition: all 0.15s; 
  white-space: nowrap;

  text-decoration: none;
  display: inline-flex;
  
  align-items: center;
}
.btn-view     { background: #1e3a5f; 
color: #93c5fd; 
}

.btn-view:hover { background: #1d4ed8;
 color: white; }

.btn-complete { 
  background: #052e16; 
color: #86efac; 
}

.btn-complete:hover { background: #16a34a; 
color: white; }
.btn-save     { background: #1d4ed8; color: white; }
.btn-save:hover:not(:disabled) { background: #2563eb; }
/* disabled ho to faded dikhega */
.btn-save:disabled { opacity: 0.4; cursor: not-allowed; }
.btn-resume   { background: #334155;
 color: #cbd5e1; }

.btn-resume:hover { background: #475569

}

/* succesyaerror msg box */
.msg-box {
  padding: 10px 14px; border-radius: 8px;
  font-size: 13px; font-weight: 500; margin-bottom: 14px;
}
.success-box { background: #052e16;
 color: #86efac; 

 border: 1px solid #166534; }
.error-box   { background: #450a0a; 
color: #fca5a5;

border: 1px solid #991b1b; 

}

/* modal ka dark overlay - click outside karo to close */
.modal-overlay {

  position: fixed; inset: 0;

  background: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(4px);  /* background blur effect */

  display: flex; align-items: 
  
  center; justify-content: center;
  z-index: 1000; padding: 20px;
}
.modal-box {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 20px;
  width: 100%; max-width: 520px;
  max-height: 88vh; overflow-y: auto;
}
/* applicatins modal thoda bada hoga*/
.large-modal {
  
  max-width: 680px;
  
  }
.modal-header
 {
  padding: 20px 24px;
  border-bottom: 1px solid #334155;
  display: flex; align-items:
   center; justify-content: space-between;
}

.modal-header h2 
{ font-size: 17px; 
font-weight: 700; 

color: #e2e8f0;

}
.modal-sub { 
  font-size: 12px;
  
  color: #64748b; margin-top: 3px; }

/* X btn modal band karne ke liye   */
.close-btn 
{
  background: #334155; 
  border: none; 
  
  border-radius: 8px;
  width: 32px; height: 32px; 
  cursor: pointer;

  font-size: 14px;
   color: #94a3b8; transition: all 0.15s


}
.close-btn:hover {
  
  background: #475569;

color: white; }
.modal-body { padding: 20px 24px; }

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid #334155;
  display: flex; justify-content: flex-end;
}

/*ek stu ka appliction card */
.app-card {
  display: flex; align-items: flex-start; 
  gap: 14px;
  padding: 16px 0; 
  border-bottom: 1px solid #334155
}
/* last card pe border nhi chiye*/
.app-card:last-child
 {
   border-bottom: none; 

 }

/* stu name ka avatar circle */
.app-avatar {
  width: 42px; height: 42px;

  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  color: white; 
  
  font-size: 18px; 
  font-weight: 700;
  border-radius: 50%;

  display: flex; 
  align-items: center; 
  justify-content: center;
  flex-shrink: 0
}

.app-info { flex: 1

}

.app-name  { font-size: 14px;

 font-weight: 700; 
 color: #e2e8f0;
 
 margin-bottom: 2px; }



/* department aor cgpa   */
.app-meta  { font-size: 12px; 

color: #64748b;
 margin-bottom: 4px; 
 }
.app-skills {
  
  font-size: 11px;
 color: #475569;
 
 }
/* right side pe statu change action */
.app-actions { display: flex; 
flex-direction: column; 
gap: 6px; 

align-items: flex-end; }


/* status drodown styling */
.status-select {
  padding: 5px 10px;
  background: #0f172a;
  border: 1px solid #334155;


  border-radius: 6px;
  color: #cbd5e1; 
  font-size: 12px;
  outline: none;
   cursor: pointer;
}


</style>