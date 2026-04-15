<template>
  <div class="wrap">

    <!-- loadng -->

    <div v-if="loading" class="loader">
      <div class="spin">

      </div>
    </div>

    <!-- header -->

    <header class="topbar">
      <div class="left">

        <div class="back" @click="$router.back()">←</div>
        <div>
          <p class="tag">Application Detail</p>
          <h1>{{ info.drive_name || 'Application' }}

          </h1>

        </div>
      </div>

      <div
       class="right">
        <span :class="['badge', getBadge(info.status)]">
          {{ info.status }}
          </span>
        <button @click="$router.push('/student-dashboard')" class="btn outline">
          
          Dashboard

        </button>
      </div>

    </header>

    <!-- body -->
    <div class="body" v-if="!loading">

      <!-- main card -->
      <div class="card">
        <div class="ctop">
          
          <div>
            <h2>{{ info.drive_name }}</h2>
            <p class="cname">{{ info.company_name }}</p>
          </div>
        </div>

        <div class="grid">
          <div class="box">
            <span class="lbl">Your Name</span>

            <span class="val">{{ info.student_name }}

            </span>

          </div>

          <div class="box">
            <span class="lbl">Email</span>
            <span class="val">{{ info.student_email }}</span>

          </div>
          <div class="box">

            <span class="lbl">Department</span>

            <span class="val">{{ info.department || 'Not set' }}

            </span>
          </div>
          <div class="box">
            <span class="lbl">CGPA</span>

            <span class="val">{{ info.cgpa || 'Not provided' }}

            </span>

          </div>
          <div class="box">

            <span class="lbl">Applied On</span>

            <span class="val">{{ info.apply_date }}</span>
          </div>

          <div class="box">
            <span class="lbl">Current Status</span>
            <span :class="['badge', getBadge(info.status)]">
              {{ info.status }}</span>
          </div>

        </div>

        <div class="skills">
          <span class="lbl">Skills</span>

          <p class="skillbox">{{ info.skills || 'No skills mentioned in profile' }}

          </p>
        </div>

        <div v-if="info.resume">

          <a :href="info.resume" target="_blank" class="btn rbtn">View Resume

          </a>

        </div>
        <div v-else class="noresume">No resume uploaded in your profile

        </div>
      </div>

      <!-- statas timelina card -->
      <div class="card">

        <h3>Application Status</h3>
        <div class="timeline">
          <div
            v-for="step in steps"
            :key="step.key"

            :class="['row', getStep(step.key)]"
          >
            <div class="dot">{{ step.icon }}</div>
            <div class="sinfo">

              <span class="slbl">{{ step.label }}</span>
              <span class="sdesc">{{ step.desc }}</span>
            </div>

          </div>
        </div>

      </div>

    </div>

  </div>

</template>

<script>

import api from "@/services/api"
;

export default {

  name: "StudentApplication",

  data() {
    return {

      loading: false,
      info: {},

      steps: 
      [
        { key: "Applied",    label: "Applied",     desc: "Your application was submitted" 

        },

        { key: "Shortlisted", 
        label: "Shortlisted",
         desc: "You have been shortlisted!"
          },
        { key: "Waitlisted", 
          label: "Waitlisted", 
           desc: "You are on the waitlist"
            },

        { key: "Rejected",    label: "Rejected",    desc: "Application was not selected" },
      ],
    };
  },

  async mounted() {
    // login check
    const token = localStorage.getItem("token");

    const role  = localStorage.getItem("role");

    if (!token || role !== "student") {
      this.$router.push("/login");
      return;
    }

    await this.getData();
  },

  methods: {

    async getData() {
      this.loading = true;
      const id = this.$route.params.appId;

      try {
        const res = await api.get(`/admin/application/${id}`);
        this.info = res.data;
      } catch (e) {

        console.error("load failed:", e);
      } 
      finally {
        this.loading = false;
      }
    },

    // badge color
    getBadge(status)
     {
      if (!status) return "";

      const s = status.toLowerCase();

      if (s === "shortlisted") 

      return "green";

      if (s === "rejected")  
        return "red";

      if (s === "waitlisted") 
       return "blue";

      return "yellow";
    },

    // timeline step state
    getStep(key) {
      const s = this.info.status;
      if (!s) return "";
      if (s === "Rejected") return key === "Rejected" ? "active" : "done";

      if (s === key) 
      return "active";
      const order = ["Applied", "Shortlisted", "Waitlisted"];

      if (order.indexOf(key) < order.indexOf(s)) return "done";

      return "";
    },

  },
};

</script>

<style scoped>

*{
  box-sizing: border-box; 

margin: 0; 
padding: 0;}

.wrap {
  min-height: 100vh;
  background: #0f172a;

  font-family: 'Inter', sans-serif;
  color: white;
  padding-bottom: 40px
}


.loader {
  position: fixed;

  inset: 0;
  background: rgba(15,23,42,0.7);
  display: flex;

  align-items: center; 
  justify-content: center;
  z-index: 9999;
}


/* upper ki side ka*/

.topbar {
  background: #1e293b;
  border-bottom: 1px solid #334155;
  padding: 18px 40px;
  display: flex;
  align-items: center; 
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap
}

.left {
  display: flex;
  align-items: center;

  gap: 14px;
}

.back {
  width: 38px; height: 38px;
  background: #334155;
  border-radius: 10px;
  display: flex;

  align-items: center; justify-content: center;
  font-size: 18px;

  cursor: pointer;
  transition: background 0.2s;
}
.back:hover { 
  background: #475569; 
  
  }

.tag 
{
  font-size: 11px;
  color: #64748b;

  text-transform: uppercase;
  letter-spacing: 0.05em
}

h1 { font-size: 20px;
 font-weight: 700; }

.right {
  display: flex;

  align-items: center;
  gap: 12px;
}

/* faltu h ab na chiye*/
.badge {
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 12px; font-weight: 700;
  white-space: nowrap;
}

.badge.green  
{ background: #052e16;

color: #86efac
 }


.badge.yellow {
  
  background: #422006; 
  color: #fde68a; }
.badge.red    { background: #450a0a;
 color: #fca5a5; }

.badge.blue  
 { 
  background: #1e3a5f; 
  color: #93c5fd
  }

/* body koi stule*/
.body {
  padding: 28px 40px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 760px;
}

.card {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 16px;
  padding: 24px;
}

.ctop {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 22px;

  padding-bottom: 18px;
  border-bottom: 1px solid #334155;
}
/* ican ki styke h*/
.icon {
  width: 50px; height: 50px;
  background: rgba(59,130,246,0.1);
  border: 1px solid rgba(59,130,246,0.3);

  border-radius: 14px;
  display: flex;
  align-items: center; 
  justify-content: center;
  font-size: 22px;
  flex-shrink: 0

}

.ctop h2 { font-size: 18px; 
font-weight: 700; 
color: #e2e8f0 }

.cname {
  font-size: 13px;
  color: #64748b;
  margin-top: 4px;
}


.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 18px;
}

.box {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.lbl {
  font-size: 10px; font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: #64748b;
}

.val {
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
}

/* skills ki design h */
.skills {
  margin-top: 4px;

  margin-bottom: 18px;
}

.skillbox {
  margin-top: 6px;
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 8px;
  padding: 12px 14px;

  font-size: 13px;
  color: #94a3b8;
  line-height: 1.65;
}

.noresume {
  font-size: 13px;
  color: #475569;
  font-style: italic;
}

/* card ki side ka style*/
.card h3 {
  font-size: 15px; 
  
  font-weight: 700;
  margin-bottom: 20px;
  color: #e2e8f0
}

.timeline {
  display: flex;
  flex-direction: column;
  gap: 0;
}
/* row ki css */
.row {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 0;

  border-bottom: 1px solid #1e293b;
  opacity: 0.35;
  transition: opacity 0.2s;

}
.row:last-child { border-bottom: none; }
.row.done   { opacity: 0.6; }
.row.active { opacity: 1; }

.dot {
  width: 36px; height: 36px;
  border-radius: 50%;
  background: #334155;
  display: flex;
  align-items: center; justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}

.row.active .dot { background: rgba(59,130,246,0.2);
 border: 2px solid #3b82f6; 
 }
.row.rejected .dot { background: rgba(220,38,38,0.15); 

border: 2px solid #dc2626; }

.sinfo {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.slbl  
{ 
  font-size: 14px; 
  
  font-weight: 700; 
  
  color: #e2e8f0; 
  }

.sdesc { 
  font-size: 12px;
   color: #64748b; }

/* btns ki design keo*/
.btn {
  padding: 9px 18px;
  border-radius: 8px;
  border: none;
  font-size: 13px; 
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap

}

.outline { background: transparent; 
border: 1px solid #60a5fa; 
color: #60a5fa; }

.outline:hover { background: rgba(96,165,250,0.1); }

.rbtn { background: #1d4ed8; color: white
}
.rbtn:hover { background: #2563eb; }




</style>