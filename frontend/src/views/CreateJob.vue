<template>
  <div class="create-job-page">

    <div class="page-header">

      <!-- dashboard pe wapas jaane ka button -->
      <button @click="$router.push('/company-dashboard')" class="back-btn"> Back to Dashboard</button>

      <h1>Create a Drive</h1>
     

    </div>


    <div class="form-card">

      <div class="form-grid">

        <!-- drive ka naam -->
        <div class="form-group">
          <label>Drive Name *</label>
          <input v-model="driveInfo.title" placeholder="e.g. SDE Internship 2025" />
        </div>


        <div class="form-group">
          <!-- job type select karo -->
          <label>Job Type *</label>
          <select v-model="driveInfo.job_type">
            <option value="">Select type</option>
            <option value="Full Time">Full Time</option>
            <option value="Internship">Internship</option>
            <option value="Part Time">Part Time</option>
            <option value="Contract">Contract</option>
          </select>
        </div>

        <div class="form-group">
          <label>Salary / Stipend *</label>
          <!-- kitna milega bhai -->
          <input v-model="driveInfo.salary" placeholder="e.g. 6 LPA or ₹15,000/month" />
        </div>


        <div class="form-group">
          <label>Application Deadline *</label>
          <input type="date" v-model="driveInfo.deadline" :min="today" />
        </div>


        <div class="form-group full-width">

          <label>Skills Required</label>

          <!-- kaunsi skills chahiye company ko -->

          <input v-model="driveInfo.skills_req" placeholder="e.g. Python, React, SQL, Communication" />

        </div>

        <div class="form-group full-width">

          <!-- poora description yahan likhna hai   -->
          <label>Job Description *</label>


          <textarea v-model="driveInfo.desc" placeholder="Describe the role, responsibilities, and what the candidate will be doing..."></textarea>
        </div>


        <div class="form-group full-width">

          <label>Eligibility Criteria</label>

          <textarea v-model="driveInfo.eligibility" placeholder="e.g. 7+ CGPA, CSE/IT/ECE branch, No active backlogs..."></textarea>
        </div>

      </div>


      <!-- error aaya toh dikhaao -->

      <div v-if="errMsg" class="msg-box error-box">{{ errMsg }} </div>

      <!-- suc msg -->
      <div v-if="successMsg" class="msg-box success-box"> {{ successMsg }}</div>


      <div class="form-actions">

        <button @click="$router.push('/company-dashboard')" class="btn btn-secondary">Cancel
        
        </button>

        <!-- sub karo drve -->

        <button @click="drivePost" :disabled="isLoading" class="btn btn-primary">
          <span v-if="isLoading" class="btn-spinner">

          </span>

          {{ isLoading ? "Posting..." : "Post Drive" }}
        </button>
      </div>


     

    </div>

  </div>

</template>

<script>

import api from "@/services/api";

export default {
  name: "CreateJob",

  data() {

    // saari initial values
    return {
      driveInfo: {
        title: "",
        job_type: "",
        desc: "",

        skills_req: "",
        salary: "",
        eligibility: "",

        deadline: ""
      },

      isLoading: false,

      errMsg: "",      // err msg store karne ke liye
      successMsg: "",  // succ pe yeh dikhega

      // aaj ki date taaki purani date select na ho sake

      today: new Date().toISOString().split("T")[0],
    };
  },

  mounted() 
  {
    // check karo ki logged in hai ya nahi
    const savedToken = localStorage.getItem("token");

    const userRole   = localStorage.getItem("role");

    if (!savedToken || userRole !== "company") {
      // login nahi hai toh wapas bhejo
      this.$router.push("/login");
      return;
    }
  },

  methods: {

    async drivePost() {

      // basic validtion pehle


      if (!this.driveInfo.title || !this.driveInfo.job_type || !this.driveInfo.deadline) 
      {

        this.errMsg = "Drive Name, Job Type and Deadline are required.";

        return;
      }

      if (!this.driveInfo.desc) {
        // description toh chahiye hi
        this.errMsg = "Job Description is required.";
        return;
      }

      if (!this.driveInfo.salary) {

        this.errMsg = "Salary/Stipend is required.";
        return;
      }

      //     sab theek hai toh loading on karo
      this.isLoading  = true;
      this.errMsg     = "";

      this.successMsg = "";

      try {

        // api call karo
        await api.post("/create_job", this.driveInfo);

        this.successMsg = "Drive posted successfully! Waiting for admin approval.";

        // form reset karo
        this.driveInfo = {
          title: "",
          job_type: "",
          desc: "",

          skills_req: "",
          salary: "",
          eligibility: "",
          deadline: ""
        };

        // thodi der baad dashboard pe jaao
        setTimeout(() => this.$router.push("/company-dashboard"), 1500);

      } catch (err) {
        // kuch gadbad hui
        this.errMsg = err.response?.data?.msg || "Could not post drive. Try again.";
      } finally {
        // loading band karo chahe error aaye ya success
        this.isLoading = false;
      }
    }

  }
};
</script>


<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.create-job-page {
  min-height: 100vh;
  background: #0f172a;
  color: white;
  font-family: 'Inter', -apple-system, sans-serif;
  padding: 0 0 60px;
}

.page-header {
  background: #1e293b;
  border-bottom: 1px solid #334155;
  padding: 20px 40px


}

/*back button stylng */
.back-btn {
  background: none;
  border: none;

  color: #60a5fa;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;

  padding: 0;
  margin-bottom: 12px;
  transition: color 0.15s;

}

.back-btn:hover
 { 
  color: #93c5fd; }

.page-header h1 {
  font-size: 22px;

  font-weight: 700;
  margin-bottom: 6px
}

.page-header p 
{
  
  font-size: 13px;


  color: #64748b
}


.form-card {
  margin: 30px 40px;
  background: #1e293b;
  border: 1px solid #334155;

  border-radius: 18px;
  padding: 32px;

  max-width: 760px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;

  gap: 20px;
  margin-bottom: 24px;
}


.form-group 
{
  display: flex;
  flex-direction: column;
  gap: 7px;
}

/* full row wale fields */
.full-width 
{ grid-column: 1 / -1

}

.form-group label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #94a3b8;
}

.form-group input,

.form-group select,

.form-group textarea {
  padding: 11px 14px;
  background: #0f172a;

  border: 1px solid #334155;
  border-radius: 9px;
  color: white;
  font-size: 14px;
  font-family: inherit;

  outline: none;
  transition: border-color 0.2s;
  
}

/* focus pe blue border */
.form-group input:focus,
.form-group select:focus,

.form-group textarea:focus {
  border-color: #3b82f6;

  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.12);
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;

  line-height: 1.6;
}

/* date picker dark mode ke liye */
.form-group input[type="date"]::-webkit-calendar-picker-indicator {
  filter: invert(1);
  cursor: pointer;
}


.msg-box {
  padding: 12px 16px;
  border-radius: 9px;

  font-size: 13px;
  font-weight: 500;
  margin-bottom: 16px

}

.error-box {
  background: #450a0a;
  color: #fca5a5;

  border: 1px solid #991b1b;
}

.success-box
 {
  background: #052e16;
  color: #86efac;
  border: 1px solid #166534;
}


.form-actions {

  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.btn {
  padding: 11px 24px;

  border-radius: 9px;
  border: none;

  font-size: 14px;
  font-weight: 600;

  cursor: pointer;
  transition: all 0.2s;
  display: flex;

  align-items: center;
  gap: 8px;
}

.btn-primary { background: #2563eb;
 color: white;
  }
.btn-primary:hover:not(:disabled)
 { background: #1d4ed8; }

/* disabled pe dull dikhe */
.btn-primary:disabled { opacity: 0.5;
 cursor: not-allowed; }

.btn-secondary { 
  background: #334155;

color: #cbd5e1; }
.btn-secondary:hover {
   background: #475569; }


/* loading spinner animation extra tha */




</style>