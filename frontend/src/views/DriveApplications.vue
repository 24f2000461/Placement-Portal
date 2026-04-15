<template>
  <div class="drive-apps-page">

    <!-- loding show karo jab tak data aaye -->

    <div v-if="pageLoading" class="load">

      <div class="spinner"></div>
    </div>


    <!-- HEADER -->
    <header class="header">

      <div class="header-left">

        <div class="back-btn" @click="$router.push('/company-dashboard')">←</div>

        <div>
          <p class="page-label">Drive Applications</p>

          <h1>{{ driveTitle || 'Applications' }}
            
          </h1>
        </div>

      </div>

      <div class="header-right">

        <!-- kitne applications aaye total -->

        <span class="count-chip">{{ appList.length }} Applications</span>

        <button @click="$router.push('/company-dashboard')" class="btn btn-outline">Back to Dashboard</button>
      </div>

    </header>


    <!-- contant AREA -->
    <div class="content">

      <!-- koi app. nahi aayi abhi tak -->
      <div v-if="!pageLoading && !appList.length" class="empty-box">

        No applications received for this drive yet.
      </div>


      <div v-for="app in appList" :key="app.id" class="app-card">

        <!-- naam ka pehla letter avatar me -->
        <div class="app-avatar">{{ app.student_name ? app.student_name[0].toUpperCase() : 'S' }}

        </div>

        <div class="app-info">

          <div class="app-name">{{ app.student_name }}</div>

          <div class="app-meta">
            {{ app.department || 'Dept. not set' }}
            {{ app.cgpa ? ' · CGPA: ' + app.cgpa : '' }}
          </div>

          <div class="app-email">{{ app.student_email }}</div>

          <div v-if="app.skills" class="app-skills">
             {{ app.skills }}</div>

        </div>


        <div class="app-right">

          <!-- current status pill -->
          <span :class="['status-pill', getStatusClass(app.status)]">{{ app.status }}</span>

          <div class="app-date">Applied: {{ app.apply_date }}

          </div>

          <div class="app-actions">

            <select v-model="app.newStatus" class="status-select">

              <option value="">Change Status</option>

              <option value="Shortlisted">Shortlist</option>

              <option value="Waitlisted">Waitlist</option>

              <option value="Rejected">Reject

              </option>
            </select>

            <button
              @click="saveStatus(app)"

              :disabled="!app.newStatus"
              class="btn btn-save"
            >
              Save
            </button>

            <!-- resume hai toh dikhao -->
            <a v-if="app.resume" :href="app.resume" target="_blank" class="btn btn-resume">
               Resume
            </a>

          </div>
        </div>

      </div>

    </div>


    <!-- toast notific. -->
    <div v-if="toastMsg" class="toast">{{ toastMsg }}</div>

  </div>
</template>


<script>

import api from "@/services/api";

export default {

  name: "DriveApplications",

  data() {

    return {

      pageLoading: false,

      // applications ki list yahan store hogi
      appList: [],

      driveTitle: "",    // drive ka naam header me dikhane ke liye

      toastMsg: "",     // success/error toast

    };
  },

  async mounted() {

    // pehle auth check karo
    const tok  = localStorage.getItem("token");

    const role = localStorage.getItem("role");

    if (!tok || role !== "company") {
      this.$router.push("/login");
      return;
    }

    // sab theek hai toh data load karo
    await this.loadApps();
  },

  methods: {

    async loadApps() {

      this.pageLoading = true;

      const dId = this.$route.params.driveId;

      try {

        const res = await api.get(`/company/drive/${dId}/applications`);

        // har application me newStatus add karo dropdown ke liye
        this.appList   = (res.data.applications || []).map(a => ({ ...a, newStatus: "" }

        )
        
        );

        this.driveTitle = res.data.job_title || "";

      } catch (e) {
        // kuch toot gaya
        this.showToast(e.response?.data?.msg || "Could not load applications");

      } finally {
        this.pageLoading = false;
      }
    },


    async saveStatus(app) {

      if (!app.newStatus) return;

      try {

        await api.post(`/company/application/${app.id}/status`, 
        { status: app.newStatus }
        
        );

        // locally bhi update karo
        app.status    = app.newStatus;
        app.newStatus = "";

        this.showToast("Status updated successfully!");


      } catch (e) {
        this.showToast(e.response?.data?.msg || "Error updating status");
      }
    },


    // status ke hisaab se css class return karo

    getStatusClass(status) {

      if (!status) return "";

      const st = status.toLowerCase();

      if (st === "shortlisted") return "pill-approved";

      if (st === "rejected")    return "pill-rejected";

      if (st === "waitlisted")  return "pill-waitlisted";

      // default pending
      return "pill-pending";
    },


    showToast(msg) {
      this.toastMsg = msg;

      // 3 sec baad hide karo
      setTimeout(() => { this.toastMsg = ""; }, 3000);
    },

  },

};
</script>


<style scoped>

* {
  box-sizing: border-box;
  margin: 0;

  padding: 0
}

.drive-apps-page {
  min-height: 100vh;
  background: #0f172a;

  font-family: 'Inter', -apple-system, sans-serif;

  color: white;
  padding-bottom: 40px;
}


/* loading ke waqt pora page cover karo */
.load {
  position: fixed;
  inset: 0;
  background: rgba(15,23,42,0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}





.header {
  background: #1e293b;
  border-bottom: 1px solid #334155;
  padding: 18px 40px;

  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 16px;
  flex-wrap: wrap;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

/* back arrow btn */
.back-btn {
  width: 38px;
  height: 38px;
  background: #334155;
  border-radius: 10px;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 18px;
  cursor: pointer;
  transition: background 0.2s;
  flex-shrink: 0;
}

.back-btn:hover { background: #475569 }

.page-label {
  font-size: 11px;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em
}

h1 {
  font-size: 20px;
  font-weight: 700
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* app. count wala blue chip */
.count-chip {
  background: rgba(59,130,246,0.15);

  color: #60a5fa;
  border: 1px solid rgba(59,130,246,0.3);
  border-radius: 20px;

  padding: 5px 14px;
  font-size: 13px;
  font-weight: 600
}


.content {
  padding: 28px 40px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.empty-box {

  text-align: center;
  padding: 60px 20px;

  color: #475569;
  font-size: 15px;
  font-style: italic
}


.app-card {
  background: #1e293b;
  border: 1px solid #334155;

  border-radius: 14px;
  padding: 20px 24px;

  display: flex;
  align-items: flex-start;
  gap: 16px;
  transition: border-color 0.2s;
}

.app-card:hover { border-color: #475569 }


/* gradiet avatar  first letter ke sath */
.app-avatar {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  color: white;

  font-size: 20px;
  font-weight: 700;
  border-radius: 50%;

  display: flex;
  align-items: center;

  justify-content: center;
  flex-shrink: 0
}

.app-info { flex: 1 }

.app-name {
  font-size: 16px;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 4px
}

.app-meta {
  font-size: 13px;

  color: #64748b;

  margin-bottom: 2px
}

.app-email {
  font-size: 12px;
  color: #475569;

  margin-bottom: 6px
}

.app-skills { font-size: 12px;
 color: #94a3b8 
 }


.app-right {
  display: flex;
  flex-direction: column;

  align-items: flex-end;
  gap: 8px;

  flex-shrink: 0;
}

.app-date {

  font-size: 11px;
  color: #475569

}

.app-actions {

  display: flex;

  align-items: center;

  gap: 8px;
  flex-wrap: wrap;
  justify-content: flex-end
}


/* STATUS PILLS - har ek ka alag color */
.status-pill {
  padding: 3px 12px;
  border-radius: 20px;

  font-size: 11px;
  font-weight: 700;

  white-space: nowrap
}

.pill-approved  
 { background: #052e16; 
 color: #86efac
  }
.pill-pending    {
   background: #422006; 
   
   color: #fde68a 
   }
.pill-rejected  
 { 
  background: #450a0a; 
  color: #fca5a5 
  }
.pill-waitlisted
 { background: #1e3a5f;
  color: #93c5fd
   }


/* common btn styles */
.btn {
  padding: 8px 16px;
  border-radius: 8px;
  border: none;

  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;

  white-space: nowrap;
  text-decoration: none;
  display: inline-flex;
  align-items: center
}

.btn-outline {
  background: transparent;
  border: 1px solid #60a5fa;
  color: #60a5fa
}

.btn-outline:hover { background: rgba(96,165,250,0.1) }

.btn-save {
  background: #1d4ed8;
  color: white;
  font-size: 12px;
  padding: 6px 12px
}

.btn-save:hover:not(:disabled) { background: #2563eb }

/* save disabled hoga jab koi status select nahi -->*/
.btn-save:disabled {
  opacity: 0.4;
  cursor: not-allowed
}

.btn-resume {
  background: #334155;
  color: #cbd5e1;
  font-size: 12px;
  padding: 6px 12px
}

.btn-resume:hover { background: #475569 }


.status-select {
  padding: 6px 10px;
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 7px;

  color: #cbd5e1;
  font-size: 12px;
  outline: none;
  cursor: pointer
}


/* neeche se aane wala toast */
.toast {
  position: fixed;
  bottom: 28px;
  left: 50%;
  transform: translateX(-50%);

  background: #1e293b;
  border: 1px solid #334155;
  color: #e2e8f0;

  padding: 12px 24px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;

  z-index: 9000;

  box-shadow: 0 4px 20px rgba(0,0,0,0.4)
}


/* mobile ke liye sab stack ho jaye */


</style>