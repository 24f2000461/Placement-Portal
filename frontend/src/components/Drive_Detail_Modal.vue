<template>
  <div v-if="show" class="modal-ov" @click="ovrlayClick">
    <div class="modal-box drv-modal">

      <!-- loading state -->
      <div v-if="loading" class="modal-load">
        <div class="spinn"></div>
        <p>Loading from database...</p>
      </div>

      <!-- actual content -->
      <template v-else>

        <!-- header -->
        <div class="modal-head">

          <h2>{{ drvData.name || 'Drive Details' }}</h2>
          <button @click="closeIt" class="cls-btn">&times;</button>
        </div>

        <!-- body -->
        <div class="modal-bdy">

          <!-- comp name -->
          <div class="comp-nm-sec">
            <h3>{{ drvData.company_name || 'Company' }}</h3>
          </div>

          <!-- job detals grid -->

          <div class="dtls-grid">

            <div class="dtl-itm full-w">
              <label>Job Title</label>
              <p class="jb-title">{{ drvData.job_title || 'N/A' }}</p>
            </div>

            <div class="dtl-itm full-w">
              <label>Job Description</label>
              <p class="jb-desc">{{ drvData.description || 'N/A' }}</p>
            </div>

            <div class="dtl-itm">
              <label>Salary</label>
              <p class="sal-val">₹{{ fmtSalary(drvData.salary) }}</p>
            </div>

            <div class="dtl-itm">
              <label>Location</label>
              <p>{{ drvData.location || 'N/A' }}</p>
            </div>

            <div class="dtl-itm">
              <label>Experience</label>

              <p>{{ drvData.experience ||
                 'N/A' }}</p>
            </div>

            <div class="dtl-itm">
              <label>Vacancies</label>
              <p>{{ drvData.vacancies ||
                 'N/A' }}
                 </p>
            </div>

            <!-- skills tags -->
            <div class="dtl-itm full-w" v-if="drvData.skills_required">
              <label>Skills Required

              </label>
              <div class="skills-row">

                <span
                  v-for="sk in drvData.skills_required.split(',')"
                  :key="sk"
                  class="sk-tag"
                >
                  {{ sk.trim()
                  
                   }}

                </span>

              </div>
            </div>

            <div class="dtl-itm">
              <label>Posted Date</label>

              <p>{{ fmtDate(drvData.posted_date) }}</p>
            </div>

          </div>

          <!-- applicatin sec-->
          <div class="apps-sec">

            <h3>Applications ({{ drvData.applications?.length 
              || 0 }})</h3>

            <!-- student tabs -->
            <div class="stu-tabs" v-if="drvData.applications?.length > 0">
              <button

                v-for="ap in drvData.applications"
                :key="ap.id"

                @click="selStu = ap"
                :class="['stu-tab', { active: selStu?.id === ap.id }]"
              >
                {{ ap.student_name }}
              </button>
            </div>

            <!-- selected stu info -->

            <div v-if="selStu" class="stu-dtls">

              <div class="inf-grid">

                <div class="inf-rw">
                  <span class="inf-lbl">Name:</span>

                  <span class="inf-val">{{ selStu.student_name }}

                  </span>
                </div>
                <div class="inf-rw">
                  <span class="inf-lbl">Department:</span>
                  <span class="inf-val">{{ selStu.department }}</span>
                </div>
                <div class="inf-rw">
                  <span class="inf-lbl">Email:

                  </span>
                  <span class="inf-val">{{ selStu.email }}</span>
                </div>
                <div class="inf-rw">
                  <span class="inf-lbl">CGPA:</span>

                  <span class="inf-val">{{ selStu.cgpa }}

                  </span>
                </div>
                <div class="inf-rw">
                  <span class="inf-lbl">Status:</span>

                  <span :class="['st-badge', selStu.status?.toLowerCase()]">
                    {{ selStu.status }}
                  </span>
                </div>

              </div>
            </div>

            <!-- koi application nhi -->
            <div v-else class="no-apps">
              <p>No applications yet</p>
            </div>

            <!-- action buttons -->
            <div class="modal-acts">
              <button @click="openResume(selStu?.resume)" class="res-btn">
                View Resume
              </button>
              <button @click="closeIt" class="bck-btn">
                Back

              </button>
            </div>

          </div>
        </div>

      </template>
    </div>

  </div>
</template>

<script>
export default {
  name: "DriveDetailModal",

  props: {
    show: {
      type: Boolean,
      default: false
    },
    // drive ka sara data prop se aata h
    driveDetails: {
      type: Object,
      default: () => ({})
    }
  },

  data() {
    return {
      loading: false,
      selStu: null, // selected student tab
    };
  },

  computed: {
    // prop ko short naam se use kro
    drvData() {
      return this.driveDetails;
    }
  },

  watch: {
    // jab naya drive data aaye toh pehla student select kro
    driveDetails: {
      immediate: true,
      handler(newVal) {
        if (newVal.applications?.length > 0) {

          this.selStu = newVal.applications[0];
        }
      }
    }
  },

  methods: {

    // salary format krna indian style
    fmtSalary(sal)
     {
      if (!sal) return 'N/A';

      return new Intl.NumberFormat('en-IN').format(sal)
      ;
    },

    // date format krna
    fmtDate(dt) {
      if (!dt) return 'N/A';

      return new Date(dt).toLocaleDateString('en-IN')
      ;
    },

    // resume open krna new tab me
    openResume(url) 
    {
      if (url) {
        window.open(url, '_blank');

      }
       else {
        alert('Resume not available');
      }
    },

    // modal band krna
    closeIt() {
      this.$emit('close')
      ;
    },

    // overlay click pe band
    ovrlayClick(e) {

      if (e.target.classList.contains('modal-ov')) 
      {
        this.closeIt();
      }
    }
  }
};
</script>

<style scoped>
/* reset */
* { box-sizing: border-box; 
margin: 0;
 padding: 0; }

/* dark overlay background */
.modal-ov {
  position: fixed;
  top: 0; left: 0; 
  right: 0; 
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center; 
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(5px);
}


.modal-box {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

/* drive modal size */
.drv-modal {
  max-width: 700px; 
  width: 90%;
  max-height: 85vh;
  overflow-y: auto;
}

/* modal header gradient */
.modal-head {
  display: flex;
  justify-content: space-between;
  
  padding: 20px 25px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 16px 16px 0 0;
   align-items: center;
  position: sticky; 
  top: 0;
   z-index: 10;
}

.modal-head h2 {
  font-size: 24px; 
  font-weight: 600; 
  color: white

}


.cls-btn {
  background: rgba(255,255,255,0.2);
  border: none; 
  color: white;
  font-size: 28px;
   cursor: pointer;
  width: 36px;
  
  height: 36px;
  border-radius: 50%;
  display: flex; 
  align-items: center;
   justify-content: center;
  transition: all 0.3s;
}
.cls-btn:hover { background: rgba(255,255,255,0.3);
 transform: rotate(90deg); }


.modal-bdy { padding: 25px; }

/* company name section */
.comp-nm-sec {
  background: #f8f9fa;
  padding: 15px 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  text-align: center;
}

.comp-nm-sec h3 {
  color: #333; 
  font-size: 20px;
  font-weight: 600;
   letter-spacing: 1px;
}


.dtls-grid {
  display: grid;
  
  
  gap: 20px;
  grid-template-columns: repeat(2, 1fr);
  margin-bottom: 30px;
}


.dtl-itm {
  background: #f8f9fa;
  padding: 15px; 
  border-radius: 10px;

  border-left: 4px solid #667eea;
}

/* full width wala item */
.full-w { grid-column: span 2
 }

.dtl-itm label {
  display: block;
  font-size: 12px; 
  color: #666;

  margin-bottom: 5px; 
  font-weight: 600;
  text-transform: uppercase; 
  letter-spacing: 0.5px;
}

.dtl-itm p { font-size: 16px;
 color: #333;
  font-weight: 500; }

/* job title big */
.jb-title { font-size: 20px;
 font-weight: 700;

 color: #2563eb; }

.jb-desc { line-height: 1.6; 
color: #4b5563; }


.sal-val { color: #059669;
 font-weight: 700;
 
 font-size: 20px; }

/* skills tags row */
.skills-row {
  display: flex;

   
  gap: 8px; 
  margin-top: 8px;
  flex-wrap: wrap;

}


.sk-tag {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4px 12px;

  border-radius: 20px;
  font-size: 12px; 
  
  font-weight: 500;
}

/* applications section */
.apps-sec {
  background: #f8f9fa;
  padding: 20px;
   border-radius: 12px;
  border: 1px solid #e5e7eb;
  margin-top: 20px;
}

.apps-sec h3 {
  color: #333;
   font-size: 18px;

    font-weight: 600;
  border-bottom: 2px solid #667eea;

  padding-bottom: 8px;
   margin-bottom: 15px
}

/* stu tabs row */
.stu-tabs {
  display: flex; 
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e5e7eb;
}

/* single student tab button */
.stu-tab {
  padding: 8px 16px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  cursor: pointer;
   font-size: 13px;
  transition: all 0.3s;
}
.stu-tab:hover { background: #e5e7eb
 }

.stu-tab.active { background: #667eea;
color: white; 
border-color: #667eea; }

/* student info box */
.stu-dtls {
  background: white;
  padding: 20px;
   border-radius: 8px;
  margin-bottom: 20px;
}


.inf-grid {
  display: grid;
  
  gap: 15px;
   margin-bottom: 20px;
   grid-template-columns: repeat(2, 1fr);
}

.inf-rw { display: flex;
 flex-direction: column; }

/* info label */
.inf-lbl { font-size: 12px; 
color: #666; 
margin-bottom: 4px; 
font-weight: 600;
 }

.inf-val { font-size: 15px; 
color: #333; 
font-weight: 500; }

/* status badge */
.st-badge {
  padding: 4px 10px; 
  border-radius: 20px;
  font-size: 11px; 
  font-weight: 600;
  text-transform: uppercase;
  display: inline-block;
}
.st-badge.applied     {
   background: #dbeafe; 
   color: #1e40af; }


.st-badge.shortlisted {
   background: #d1fae5; 
   color: #065f46; 
   }

.st-badge.rejected    {
   background: #fee2e2; 
   color: #991b1b; }
.st-badge.selected    { 
  background: #fef3c7; color: #92400e; }

/* no apps empty state */
.no-apps {
  text-align: center; 
  padding: 40px;
  background: #f9fafb; 
  border-radius: 8px;
  color: #6b7280;
}

/* action buttons bottom */
.modal-acts {
  display: flex;
   gap: 15px;
  
  margin-top: 20px; 
  padding-top: 15px;
  border-top: 1px solid #e5e7eb;
  justify-content: flex-end;
}

/* view resume button */
.res-btn {
  background: #2563eb; 
  color: white;
  border: none; 
  padding: 10px 24px;
  border-radius: 8px; 
  cursor: pointer;
  font-weight: 600; 
  transition: all 0.3s;
}
.res-btn:hover:not(:disabled) {
  background: #1d4ed8;

  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(37,99,235,0.3)
}
.res-btn:disabled { background: #9ca3af; 
cursor: not-allowed; 
}

/* back button */
.bck-btn {
  background: #6b7280; 
  color: white;
  border: none; 
  padding: 10px 24px;
  border-radius: 8px; 
  cursor: pointer;
  font-weight: 600; 
  transition: all 0.3s;
}
.bck-btn:hover { background: #4b5563;
 transform: translateY(-2px); }

/* loading state */
.modal-load {
   padding: 60px; 
   text-align: center; }

/* loading spinner */



</style>