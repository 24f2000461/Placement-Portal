<template>
  <div class="student-pg">

    <!-- loading wala part -->

    <div v-if="pgLoading" class="load-overlay">
      <div class="spinn"></div>

    </div>

    <!-- mein dash-->
    <div v-if="currScreen === 'main'">
      <header class="topbar">
        <div class="left-side">

          <div class="av">{{ getInitials }}

          </div>

          <div>

            <h1>
              Welcome, {{ student.studentName || student.name || 'Student' }}
              </h1>

            <p class="sub-head">{{ student.department || 'Department not set' }}

            </p>
          </div>

        </div>
        <div class="nav-links">
          <span @click="currScreen = 'applications'" class="nl">Applications

          </span>
          <span class="divdr">|

          </span>


          <span @click="currScreen = 'editProfile'" class="nl">Edit Profile</span>
          <span class="divdr">|</span>

          <span @click="doLogout" class="nl red-nl">Logout

          </span>
        </div>

      </header>

      <div class="pg-body">

        <!-- search bar -->
        <div class="srch-wrap">
          <span class="srch-ico">🔍</span>
          <input
            v-model="srchQ"

            type="text"
            placeholder="Search companies by name, industry..."

            class="srch-inp"
          />

          <button v-if="srchQ" @click="srchQ = ''" class="clr-btn">✕

          </button>
        </div>

        <!-- company lst -->

        <div class="sec">

          <h2 class="sec-head">Organizations</h2>

          <div v-if="dataLoading" class="empty-bx">Loading companies...</div>

          <div v-else-if="!companiesFiltered.length" class="empty-bx">

            {{ srchQ ? 'No companies match your search' : 'No companies available right now' }}
          </div>

          <div v-else>

            <div v-for="comp in companiesFiltered" :key="comp.company_id" class="list-rw">
              <div 
              class="rw-info">

                <span class="rw-nm">{{ comp.company_name }}

                </span>

                <span class="rw-mt">{{ comp.industry }} {{ comp.location ? '· ' + comp.location : '' }}</span>
              </div>

              <button @click="openComp(comp)" class="act-btn">View Details</button>
            </div>

          </div>
        </div>

        <!-- applied drives sec -->

        <div class="sec">
          <h2 class="sec-head">
            Applied Drives</h2>

          <div class="tbl-wrap">
            <table class="dtbl">

              <thead>
                <tr>
                  <th>Sr No.</th>
                  <th>Drive Name</th>

                  <th>Company</th>
                  <th>Date</th>
                  <th>Status</th>

                  <th>Action</th>
                </tr>
              </thead>
              <tbody>

                <tr v-if="!allApps.length">

                  <td colspan="6" class="emptytd">No applied drives yet. Browse companies above!</td>
                </tr>

                <tr v-for="(ap, idx) in last3Apps" :key="ap.app_id">
                  <td class="muted-td">{{ idx + 1 }}.

                  </td>
                  <td 
                  class="bld-td">{{ ap.job_title }}

                  </td>

                  <td>{{ ap.company_name }}

                  </td>

                  <td class="muted-td">{{ ap.date }}</td>

                  <td>
                    <span :class="['st-pill', getPillClass(ap.status)]">{{ ap.status }}

                    </span>
                  </td>

                  <td>
                    <button @click="currScreen = 'applications'" class="sm-btn">View All</button>
                  </td>
                </tr>

              </tbody>
            </table>
          </div>

          <div v-if="allApps.length > 3" class="more-wrap">
            <button @click="currScreen = 'applications'" class="lnk-btn">
              View all {{ allApps.length }} applications →
            </button>
          </div>

        </div>
      </div>
    </div>

    <!--company detil -->

    <div v-if="currScreen === 'company'">
      <header class="topbar">
        <div class="left-side">

          <div class="comp-logo">{{ selComp.company_name ? selComp.company_name[0] : 'C' }}</div>
          <div>
            <p class="pg-lbl">Company</p>

            <h1>{{ selComp.company_name }}</h1>
          </div>
        </div>
        <div class="nav-links">
          <span @click="currScreen = 'applications'" class="nl">Applications

          </span>
          <span class="divdr">|</span>
          <span @click="currScreen = 'main'" class="nl">← Back</span>
        </div>
      </header>

      <div class="pg-body">

        <!-- overview part -->
        <div class="ovrvw-sec">

          <h3 class="sec-head">Overview</h3>

          <p class="ovrvw-txt">{{ selComp.des || 
            'No company description available.' }}</p>

          <div class="chip-row">

            <div v-if="selComp.industry" class="chip">
              <span class="chip-k">Industry


              </span>

              <span class="chip-v">{{ selComp.industry }}</span>
            </div>
            <div v-if="selComp.location" class="chip">
              <span class="chip-k">Location</span>

              <span class="chip-v">{{ selComp.location }}

              </span>
            </div>
            <div v-if="selComp.comp_size" class="chip">
              <span class="chip-k">Size</span>
              <span class="chip-v">{{ selComp.comp_size }}</span>

            </div>
            <a v-if="selComp.website" :href="selComp.website" target="_blank" class="chip chip-lnk">
              <span class="chip-k">Website</span>
              <span class="chip-v chip-blue">{{ selComp.website }}</span>
            </a>

          </div>

        </div>

        <h3 class="sec-head">Current Drives</h3>

        <div v-if="compLoading" class="empty-bx">Loading drives...</div>
        <div v-else-if="!compDrives.length" class="empty-bx">No active drives for this company right now</div>

        <div v-else>
          <div v-for="jb in compDrives" :key="jb.id" class="list-rw">
            <div class="rw-info">
              <span class="rw-nm">{{ jb.title }}</span>

              <span class="rw-mt">{{ jb.job_type }} · 
                {{ jb.salary }} · Due: 
                {{ jb.deadline }}
                </span>

            </div>

            <button @click="openDrv(jb)" class="act-btn">
              View Details</button>
          </div>
        </div>

        <button @click="currScreen = 'main'" class="back-full-btn">Back

        </button>
      </div>
    </div>

    <!--drive detail  -->
    <div v-if="currScreen === 'drive'">


      <header class="topbar">
        <div class="left-side">
          <div>
            <p class="pg-lbl">Drive Detail</p>

            <h1>{{ selDrive.title }}</h1>
          </div>
        </div>
        <div class="nav-links">
          <span @click="currScreen = 'company'" 
          class="nl">← Back</span>
        </div>

      </header>

      <div class="pg-body">

        <div class="drv-card">

          <div class="drv-body">

            <div class="drv-lft">
              <div class="fld-blk">
                <span class="fld-lbl">Job Title</span>

                <span class="fld-val">{{ selDrive.title }}</span>

              </div>
              <div class="fld-blk">
                <span class="fld-lbl">Job Type</span>

                <span class="fld-val">{{ selDrive.job_type || 'N/A' }}</span>
              </div>
              <div class="fld-blk">
                <span class="fld-lbl">Salary / Stipend</span>
                <span class="fld-val grn-val">{{ selDrive.salary || 'N/A' }}</span>
              </div>
              <div class="fld-blk">
                <span class="fld-lbl">Location</span>

                <span class="fld-val">{{ selDrive.location 
                  || selComp.location || 'N/A' }}</span>

              </div>
              <div class="fld-blk">

                <span class="fld-lbl">Application Deadline</span>
                <span class="fld-val rd-val">{{ selDrive.deadline || 'N/A' }}</span>
              </div>
              <div class="fld-blk">
                <span class="fld-lbl">Skills Required</span>

                <span class="fld-val">{{ selDrive.skills_req || 'N/A' }}</span>
              </div>
              <div class="fld-blk">
                <span class="fld-lbl">
                  Eligibility</span>
                <span class="fld-val">{{ selDrive.eligibility ||
                   'Not specified' }}</span>
              </div>
              <div class="fld-blk">
                <span class="fld-lbl">Job Description</span>

                <p class="fld-desc">{{ selDrive.desc || 'No description provided.' }}</p>
              </div>
            </div>

            <!-- right side company widget -->
            <div class="drv-rgt">
              <div class="comp-widget">
                <div class="circles">
                  <div class="circ c-red"></div>

                  <div class="circ c-teal"></div>

                  <div class="circ c-blue"></div>
                </div>
                <p class="comp-nm-lbl">{{ selComp.company_name }}</p>

                <p class="comp-mt">{{ selComp.industry }}</p>
                <p class="comp-mt">{{ selComp.location }}</p>

              </div>
            </div>

          </div>

          <!-- apply button area -->
          <div class="drv-acts">
            <button
              @click="doApply"
              :disabled="isApplied || applyingNow"

              :class="['apply-btn', isApplied ? 'already-applied' : '']"
            >
              <span v-if="applyingNow" class="btn-spn"></span>

              {{ applyingNow ? 'Applying...' : isApplied ? 
              ' Already Applied' : 'Apply Now' }}
            </button>

            <button @click="currScreen = 'company'" class="go-back-btn">Go Back</button>
          </div>

        </div>
      </div>
    </div>

    <!-- applications his -->
    <div v-if="currScreen === 'applications'">

      <header class="topbar">
        <div class="left-side">

          <div class="av">{{ getInitials }}</div>
          <div>
            <h1>Application History</h1>
            <p class="sub-head">{{ student.studentName 
              || student.name }} · {{ student.department || 'N/A' }}</p>

          </div>
        </div>

        <div class="nav-links">
          <span @click="currScreen = 'main'" class="nl">
             Dashboard</span>
        </div>
      </header>

      <div class="pg-body">
        <div class="tbl-wrap">
          <table class="dtbl">

            <thead>
              <tr>
                <th>Drive No.</th>
                <th>Interview</th>
                <th>Job Title</th>

                <th>Company</th>
                <th>Applied On</th>
                <th>Result</th>

              </tr>
            </thead>

            <tbody>

              <tr v-if="!allApps.length">
                <td colspan="6" class="emptytd">No application history. Start applying to drives!</td>
              </tr>

              <tr v-for="(ap, idx) in allApps" :key="ap.app_id">

                <td class="muted-td">{{ idx + 1 }}.</td>
                <td class="muted-td">
                  In-person</td>
                <td class="bld-td">
                  {{ ap.job_title }}</td>
                <td>{{ ap.company_name }}</td>

                <td class="muted-td">{{ ap.date }}</td>
                <td>
                  <span :class="['st-pill', getPillClass(ap.status)]">{{ ap.status }}

                  </span>
                </td>

              </tr>

            </tbody>
          </table>

        </div>
      </div>
    </div>

    <!-- edit pro -->
    <div v-if="currScreen === 'editProfile'">

      <header class="topbar">
        <div class="left-side">
          <div class="av">{{ getInitials }}</div>
          <div>
            <h1>Edit Profile</h1>
            <p class="sub-head">{{ student.studentName || student.name }}</p>
          </div>
        </div>
        <div class="nav-links">
          <span @click="currScreen = 'main'" class="nl">← Dashboard</span>
        </div>
      </header>

      <div class="pg-body">

        <div v-if="profMsg" :class="['prof-msg', profMsgTyp]">{{ profMsg }}</div>

        <div class="prof-grid">

          <!-- academic wala card -->
          <div class="prof-card">
            <h3 class="prof-card-head">📋 Academic Details</h3>

            <div class="fg">
              <label>Full Name</label>
              <input v-model="profEdit.name" disabled class="dis-inp" />
            </div>
            <div class="fg">
              <label>Department / Branch</label>
              <input v-model="profEdit.department" 
              placeholder="e.g. Computer Science and Engineering" />

            </div>
            <div class="fg">

              <label>CGPA</label>
              <input v-model="profEdit.cgpa" 
              type="number" step="0.01" min="0" max="10" 
              placeholder="e.g. 8.5" />
            </div>
            <div class="fg">
              <label>Education</label>
              <textarea v-model="profEdit.education" 
              placeholder="e.g. B.Tech CSE, XYZ University, 2021-2025"></textarea>
            </div>

          </div>

          <!-- skills resume wala card -->
          <div class="prof-card">
            <h3 class="prof-card-head">
               Skills & Resume</h3>

            <div class="fg">
              <label>Skills (comma-separated)</label>

              <textarea v-model="profEdit.skills" placeholder="e.g. Python, Machine Learning, React, SQL, Communication"></textarea>
            </div>
            <div class="fg">

              <label>Resume Link (Google Drive / Portfolio)</label>
              <input v-model="profEdit.resume" 
              placeholder="https://drive.google.com/..." />
            </div>

            <div v-if="profEdit.resume" class="res-prev">
              <span>📎 Resume linked</span>

              <a :href="profEdit.resume" target="_blank" class="res-lnk">View Resume →</a>
            </div>

          </div>
        </div>

        <!-- save cancel btn-->
        <div class="prof-acts">
          <button @click="currScreen = 'main'" class="btn btn-sec">Cancel

          </button>

          <button @click="saveProf" :disabled="savingProf" 
          class="btn btn-pri">

            <span v-if="savingProf" class="btn-spn"></span>
            {{ savingProf ? 'Saving...' : 'Save Profile' }}

          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "StudentDashboard",

  data() {
    return {
      // loading states
      pgLoading: false,
      dataLoading: false,

      compLoading: false,
      applyingNow: false,

      // screen control
      currScreen: "main",
      srchQ: "",

      // data
      student: {},
      companyList: [],
      allApps: [],

      // selected wale
      selComp: {},
      compDrives: [],

      selDrive: {},

      // profile edit form ka data

      profEdit: { name: "", department: "", 
      cgpa: "", 
      skills: "", 
      education: "", resume: ""
       },
      profMsg: "",
      profMsgTyp: "succ-msg",
      savingProf: false,
    };
  },

  computed: {

    // initials nikalta h naam se
    getInitials() {
      const nm = this.student.studentName || this.student.name || "";
      return nm.split(" ").map(n => n[0]).join("").toUpperCase().slice(0, 2);
    },

    // search filter
    companiesFiltered() {
      if (!this.srchQ.trim()) return this.companyList;
      const q = this.srchQ.toLowerCase();

      return this.companyList.filter(c =>
        c.company_name?.toLowerCase().includes(q) ||

        c.industry?.toLowerCase().includes(q) ||
        c.location?.toLowerCase().includes(q)
      );
    },

    // sirf 3 dikha dashboard pe
    last3Apps() {
      return this.allApps.slice(0, 3);

    },

    // check kro pehle apply kiya h ya nhi
    isApplied() {
      return this.allApps.some(a => a.job_id === this.selDrive.id);

    },
  },

  async mounted() {
    const token = localStorage.getItem("token");
    const role  = localStorage.getItem("role");

    if (!token || role !== "student") { this.$router.push("/login"); return; }
    await this.loadEverything();
  },

  methods: {

    // sab kuch load kro ek sath
    async loadEverything() {
      this.pgLoading = true;
      try {
        const [profRes, appsRes] = await Promise.all([
          api.get("/student/profile"),
          api.get("/student/applications"),
        ]);
        this.student  = profRes.data;
        this.profEdit = { ...profRes.data };
        this.allApps  = appsRes.data;

        await this.fetchComps();
      } catch (e) {
        console.error("Load error:", e);
      } finally {
        this.pgLoading = false;
      }
    },

    // companies fetch krna
    async fetchComps() {
      this.dataLoading = true;
      try {
        const res = await api.get("/student/companies"
        );
        this.companyList = res.data;
      } catch (e) 
      {
        console.error("Companies error:", e);
      } finally {
        this.dataLoading = false;
      }
    },

    // company open kro aur uske drives bhi lo
    async openComp(comp) {
      this.selComp = comp;
      this.currScreen = "company";
      this.compLoading = true;
      try {
        const res = await api.get(`/student/company/${comp.company_id}`);
        this.selComp   = { ...comp, ...res.data };
        this.compDrives = res.data.jobs || [];
      } catch (e) {
        this.compDrives = [];
      } finally {
        this.compLoading = false;
      }
    },

    // drive open krna
    openDrv(jb) {
      this.selDrive  = jb;
      this.currScreen = "drive";
    },

    // apply kro job me
    async doApply() {
      if (this.isApplied) return;
      this.applyingNow = true;
      try {
        await api.post(`/student/apply/${this.selDrive.id}`);
        const appsRes = await api.get("/student/applications");
        this.allApps = appsRes.data;
        alert(" Applied successfully!");
      } catch (e) {
        alert(e.response?.data?.msg || "Could not apply. Try again.");
      } finally {
        this.applyingNow = false;
      }
    },

    // profile save krna
    async saveProf() {
      this.savingProf = true;
      this.profMsg = "";
      try {
        await api.put("/student/profile", {
          department: 
          this.profEdit.department,
          cgpa:     
            this.profEdit.cgpa,
          skills:    
          
          this.profEdit.skills,

          education:  
          this.profEdit.education,

          resume:  

          this.profEdit.resume,

        }
        );
        this.student = { ...this.student, ...this.profEdit };
        this.profMsg    = "Profile updated successfully!";

        this.profMsgTyp = "succ-msg";
        setTimeout(() => { this.profMsg = ""; this.currScreen = "main"; }, 1500);
      } catch (e) {
        this.profMsg    = e.response?.data?.msg || "Error saving profile";
        this.profMsgTyp = "err-msg";
      } finally {
        this.savingProf = false;
      }
    },

    // status ka color decide krta h
    getPillClass(status) {
      if (!status)
       return "";
      const s = status.toLowerCase();
      if (s === "shortlisted")
       return "pill-ok";

      if (s === "rejected")  
        return "pill-no";

      if (s === "waitlisted") 
       return "pill-wait";

      return "pill-pend";
    },

    // logout
    doLogout() {
      localStorage.clear();
      this.$router.push("/login");
    },
  }
};
</script>

<style scoped>
/* reset basic */
* { box-sizing: border-box;
 margin: 0; padding: 0 }

/* main page wrap */
.student-pg {
  min-height: 100vh;
  background: #f4f6fb;

  font-family: 'Inter', -apple-system, sans-serif;
  color: #1e293b;

  padding-bottom: 60px;
}

/* loading overlay */
.load-overlay
 {
  position: fixed;


  inset: 0;
  background: rgba(244,246,251,0.85);
  display: flex;
  align-items: center; 
  justify-content: center;
  z-index: 9999
}

/* loading spinner */


/* header topbar */
.topbar {
  background: white;
  border-bottom: 1px solid #e2e8f0;

  padding: 16px 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  position: sticky; top: 0; z-index: 10;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05)

}

/* left wala header */
.left-side { display: 

flex; align-items: center; gap: 14px; }

/* avatar circle */
.av {
  width: 46px; height: 46px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);

  color: white; font-size: 18px; font-weight: 800;
  border-radius: 50%;

  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}

/* company logo square */
.comp-logo {
  width: 46px; height: 46px;

  background: linear-gradient(135deg, #0f172a, #334155);
  color: white; font-size: 20px; font-weight: 800;
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0

}

.left-side h1 { font-size: 20px; 
font-weight: 700; 
color: #0f172a; 
}
.sub-head 
{
   font-size: 13px; 
   
   color: #64748b; margin-top: 2px; }

/* page label chhota wala */

.pg-lbl { font-size: 11px; 
color: #94a3b8; 

font-weight: 600;
 text-transform: uppercase;
  letter-spacing: 0.06em; 
  margin-bottom: 2px; }

/* nav area right side */
.nav-links { display: flex; 
align-items: center; 
gap: 8px}

.nl {
  font-size: 13px; 
  font-weight: 600;
  color: #3b82f6;
   cursor: pointer;
  transition: color 0.15s;
}
.nl:hover { color: #1d4ed8;
 }

/* logout ka red */
.red-nl { color: #dc2626 }

.red-nl:hover { color: #b91c1c; 
}

.divdr { color: #e2e8f0; 
font-size: 14px; }

/* body content ka wrap */
.pg-body { padding: 28px 40px;
 max-width: 1100px; 
 }

/* search bar */
.srch-wrap {
  display: flex; align-items: center; gap: 10px;
  background: white;
  border: 1.5px solid #e2e8f0;

  border-radius: 12px;
  padding: 10px 16px;

  margin-bottom: 28px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  transition: border-color 0.2s;
}
.srch-wrap:focus-within { border-color: #3b82f6; 
box-shadow: 0 0 0 3px rgba(59,130,246,0.10); }

.srch-ico { font-size: 16px; 
color: #94a3b8; }

.srch-inp {
  flex: 1; border: none;
   outline: none;
  font-size: 14px;
  
  color: #1e293b; background: transparent;
}
.srch-inp::placeholder { color: #94a3b8; }

/* cross button search clear */
.clr-btn {
  background: #f1f5f9; 
  border: none; 
  
  border-radius: 6px;
  width: 24px;
   height: 24px;
    cursor: pointer;
  color: #64748b; 
  font-size: 12px;
  transition: all 0.15s;
}
.clr-btn:hover { background: #e2e8f0; }

/* section wrap */
.sec { margin-bottom: 36px; }

/* section heading */
.sec-head { font-size: 14px; 
font-weight: 700; 
color: #0f172a; 
text-transform: uppercase;
 letter-spacing: 0.06em;
  margin-bottom: 14px; }

/* list row company ya drive */
.list-rw {
  display: flex; 
  align-items: center;
  justify-content: space-between;

  background: white;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;

  padding: 14px 18px;
  margin-bottom: 8px;
  gap: 12px;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.list-rw:hover { border-color: #3b82f6; 

box-shadow: 0 4px 12px rgba(59,130,246,0.08);
 }

.rw-info { display: flex; 
flex-direction: column; 
gap: 3px;
 }


.rw-nm 

{ font-size: 14px;
 font-weight: 600; 
 
color: #1e293b}

.rw-mt { font-size: 12px;
 color: #64748b; }

/* view details button */
.act-btn {
  padding: 7px 18px;
  background: #eff6ff;
   color: #2563eb;
  border: 1.5px solid #bfdbfe;

  border-radius: 8px;
  font-size: 13px;
   font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}
.act-btn:hover { background: #2563eb; 
color: white; 
border-color: #2563eb; 
}

/* table ka wrapper */
.tbl-wrap {
  background: white;
  border: 1.5px solid #e2e8f0;
  border-radius: 14px;
  overflow: hidden; 
  overflow-x: auto;
}

/* table */
.dtbl { width: 100%;
 border-collapse: collapse;
  font-size: 13px; }

/* table header */
.dtbl th {
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

.dtbl td {
  padding: 12px 16px;
  border-bottom: 1px solid #f1f5f9;
  color: #374151;
   vertical-align: middle;
}

.dtbl tr:last-child td { border-bottom: none; 
}
.dtbl tr:hover td { background: #f8fafc; 
}

/* muted text */
.muted-td { color: #94a3b8; }
.bld-td { font-weight: 600; color: #1e293b
 }

/* empty table msg */
.emptytd { text-align: center; 
padding: 32px; color: #94a3b8;
 font-style: italic; }

/* empty box */
.empty-bx {
  background: white;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  padding: 28px; 
  text-align: center;
  color: #94a3b8;
   font-size: 13px;
}

/* view more wrap */
.more-wrap { text-align: center;
 margin-top: 10px; }

.lnk-btn {
  background: none; 
  border: none;
  color: #3b82f6; 
  font-size: 13px; 
  font-weight: 600;
  cursor: pointer;
}
.lnk-btn:hover
 { text-decoration: underline; }

/* chhota wala button */
.sm-btn {
  padding: 5px 12px;
  background: #eff6ff; 
  color: #2563eb;
  border: 1px solid #bfdbfe;
  border-radius: 6px;
  font-size: 11px;
   font-weight: 600;
  cursor: pointer; 
  transition: all 0.15s;
}
.sm-btn:hover { background: #2563eb; 
color: white; 
border-color: #2563eb; }

/* status pills */
.st-pill {
  padding: 3px 10px; 
  border-radius: 20px;
  font-size: 11px;
   font-weight: 700;
  white-space: nowrap;
}
.pill-ok   { background: #f0fdf4; 
color: #16a34a; 
border: 1px solid #bbf7d0;
 }

.pill-no   { background: #fef2f2; 
color: #dc2626; 

border: 1px solid #fecaca; }

.pill-pend { background: #fffbeb; 
color: #d97706; 
border: 1px solid #fde68a }
.pill-wait { background: #eff6ff; 
color: #2563eb; 
border: 1px solid #bfdbfe; }

/* overview section */
.ovrvw-sec { margin-bottom: 28px; }

/* overview text box */
.ovrvw-txt {
  font-size: 14px; color: #374151; 
  line-height: 1.7;
  background: white;
  border: 1.5px solid #e2e8f0; 
  border-radius: 12px;
  padding: 16px 18px; 
  margin-bottom: 14px;
}

/* chips row */
.chip-row { display: flex; 
flex-wrap: wrap; 
gap: 8px; 
margin-bottom: 20px;

}

.chip {
  display: inline-flex;
   align-items: center; 
   gap: 6px;
  background: white;
  border: 1.5px solid #e2e8f0;
  padding: 6px 14px; 
  border-radius: 20px;
}

.chip-lnk { text-decoration: none; 
cursor: pointer; }

.chip-lnk:hover { border-color: #3b82f6; }

.chip-k { font-size: 10px; 
font-weight: 700; 
text-transform: uppercase; 
letter-spacing: 0.07em; 

color: #94a3b8; }
.chip-v { font-size: 12px; 
font-weight: 600; 
color: #1e293b; }

.chip-blue { color: #3b82f6
 }

/* drive detail card */
.drv-card {
  background: white;
  border: 1.5px solid #e2e8f0;
  border-radius: 16px; 
  padding: 28px;
}

.drv-body { display: flex; 
gap: 32px;
 margin-bottom: 24px; }

/* left side drive info */
.drv-lft { flex: 1; 
display: flex;
 flex-direction: column; 
 gap: 14px; }

.fld-blk { display: flex;

flex-direction: column;
 gap: 4px; }

/* field label */
.fld-lbl { font-size: 10px; 
font-weight: 700; 
text-transform: uppercase; 
letter-spacing: 0.07em; 
color: #94a3b8; }

.fld-val 
{ font-size: 14px; 
font-weight: 600; 
color: #1e293b; }

.fld-desc {
  font-size: 13px;
   color: #64748b; 
   line-height: 1.65;
  background: #f8fafc; 
  padding: 10px 12px;
  border-radius: 8px; 
  border: 1px solid #e2e8f0;
}

.grn-val {
  
  color: #16a34a; }

.rd-val  { color: #dc2626; }

/* right side co widget */
.drv-rgt { flex-shrink: 0; }

.comp-widget {
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 14px; padding: 20px 22px;
  text-align: center; width: 180px;
}

/* 3 colored circles */
.circles { display: flex; 
justify-content: center; 
margin-bottom: 10px; }

.circ {
  width: 30px; height: 30px;
  border-radius: 50%;
  border: 2px solid white;
  margin-left: -6px;
}
.circ:first-child { margin-left: 0; }

.c-red  { 
  background: #ef4444; }
.c-teal { background: #0d9488; }
.c-blue { 
  background: #3b82f6; }

.comp-nm-lbl { font-size: 11px;
 font-weight: 700; color: #1e293b;
  text-transform: uppercase;
   letter-spacing: 0.06em; 
   margin-bottom: 4px; }

.comp-mt { font-size: 11px;
 color: #94a3b8; }

/* apply area buttons */
.drv-acts {
  display: flex; 
  align-items: center;
   gap: 12px;
  padding-top: 20px;
  border-top: 1.5px solid #f1f5f9;
}

/* apply button */
.apply-btn {
  padding: 11px 28px;
  background: #2563eb;
   color: white;
  border: none; 
  border-radius: 10px;
  font-size: 14px; 
  
  font-weight: 700;
  cursor: pointer; 
  transition: all 0.2s;
  display: flex;
   align-items: center;
    gap: 8px;
}
.apply-btn:hover:not(:disabled)
 { background: #1d4ed8;
 
 }
.apply-btn:disabled { 
  opacity: 0.6; 
  cursor: not-allowed; }

/* already applied green */
.already-applied { 
  background: #16a34a !important; 
  opacity: 1 !important; 
  cursor: default !important; }

/* go back button */
.go-back-btn {
  padding: 11px 22px;
  background: #f1f5f9; 
  color: #374151;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  font-size: 14px;
   font-weight: 600;
  cursor: pointer; 
  transition: all 0.2s;
}
.go-back-btn:hover { background: #e2e8f0; }

/* back full width button */
.back-full-btn {
  display: inline-block; 
  margin-top: 24px;
  padding: 10px 20px;
  background: #f1f5f9; 
  color: #374151;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  font-size: 14px;
   font-weight: 600;
  cursor: pointer;
   transition: all 0.2s;
}
.back-full-btn:hover { background: #e2e8f0; }

/* profile msg success or error */
.prof-msg {
  padding: 12px 16px; 
  border-radius: 10px;
  font-size: 13px; 
  font-weight: 500;
  margin-bottom: 20px;
}
.succ-msg { background: #f0fdf4; 
color: #16a34a; 

border: 1px solid #bbf7d0

}
.err-msg  { background: #fef2f2; 
color: #dc2626; 

border: 1px solid #fecaca; }

/* profile 2 col grid */
.prof-grid { display: grid;
 grid-template-columns: 1fr 1fr;
  gap: 20px; 
  margin-bottom: 24px; }

/* profile card */
.prof-card {
  background: white;
  border: 1.5px solid #e2e8f0;
  border-radius: 14px;
   padding: 24px;
}

.prof-card-head { font-size: 14px;
 font-weight: 700;
  color: #0f172a; 
  margin-bottom: 18px; }

/* form group */
.fg { margin-bottom: 16px; }

.fg label {
  display: block;
  font-size: 11px; 
  font-weight: 700;
  text-transform: uppercase;
   letter-spacing: 0.06em;
  color: #94a3b8; 
  margin-bottom: 6px;
}

.fg input,

.fg textarea {
  width: 100%; 
  
  padding: 10px 14px;
  border: 1.5px solid #e2e8f0;
  border-radius: 9px;
  font-size: 13px;
   color: #1e293b;
  outline: none;
  background: #f8fafc; 
  font-family: inherit;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.fg input:focus,
.fg textarea:focus
 {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59,130,246,0.10);
  background: white;
}
.fg textarea { resize: vertical; 
min-height: 80px; }

/* disabled input */
.dis-inp { background: #f1f5f9 !important; 
color: #94a3b8 !important; 
cursor: not-allowed; }

/* resume link previw */
.res-prev {
  display: flex; 
  align-items: center;
  
  justify-content: space-between;
  padding: 10px 14px;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 8px;
  font-size: 13px; color: #16a34a;
}
.res-lnk { font-size: 12px;
 font-weight: 600;
  color: #16a34a; 
 text-decoration: none; }

.res-lnk:hover { text-decoration: underline
 }

/* profile save cancel */
.prof-acts { display: flex; 
gap: 12px; }

/* generic btn */
.btn {
  padding: 10px 22px;
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

.btn-pri { background: #2563eb; 
color: white;
 
 }

.btn-pri:hover:not(:disabled) 
{ background: #1d4ed8; }

.btn-pri:disabled { opacity: 0.6;
 cursor: not-allowed; }

.btn-sec { background: #f1f5f9; 
color: #374151;
 border: 1.5px solid #e2e8f0; }
.btn-sec:hover { background: #e2e8f0; }

/* small spinner inside button */
.btn-spn {
  width: 14px; 
  height: 14px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spinit 0.7s linear infinite;
}
</style>