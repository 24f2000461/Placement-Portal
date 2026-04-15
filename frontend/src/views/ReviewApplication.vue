<template>
  <div class="wrap">

    <!-- loading -->
    <div v-if="loading" class="loader">

      <div class="spin"></div>
    </div>

    <!-- header -->
    <header class="topbar">

      <div class="left">

        <div class="back" @click="$router.back()">

        </div>

        <div>
          <p class="tag">
            Review Application
            </p>

          <h1>{{ info.student_name || 'Student Application' }}</h1>
        </div>

      </div>

      <div class="right">

        <span :class="['badge', getBadge(info.status)]">
          
          {{ info.status }}

        </span>

        <button @click="$router.back()"
         class="btn outline">Back
         
         </button>

      </div>

    </header>


    <!-- page body -->
    <div class="body" v-if="!loading">

      <!-- student card -->
      <div class="card">

        <div class="stop">

          <div class="avatar">

            {{ info.student_name ? info.student_name[0].toUpperCase() : 'S' }}

          </div>

          <div>

            <h2 class="sname">{{ info.student_name }}</h2>

            <p class="semail">{{ info.student_email }}</p>

            <p class="sdept">{{ info.department || 'Department not set' }}</p>
          </div>

        </div>

        <!-- info boxes -->
        <div class="grid">

          <div class="box">

            <span class="lbl">Drive Applied</span>
            <span class="val">{{ info.drive_name }}</span>
          </div>
          <div class="box">
            <span class="lbl">Company</span>

            <span class="val">{{ info.company_name }}</span>
          </div>
          <div class="box">
            <span class="lbl">CGPA</span>

            <span class="val">{{ info.cgpa || 'Not provided' }}</span>

          </div>

          <div class="box">
            <span class="lbl">
              Applied On
              </span>

            <span class="val">
              {{ info.apply_date }}

            </span>
          </div>
        </div>

        <!-- skills -->
        <div class="skills">
          <span class="lbl">Skills

          </span>

          <p class="skillbox">{{ info.skills || 'No skills mentioned' }}</p>
        </div>
      </div>


      <!-- act card -->
      <div class="card">

        <h3>Update Application Status</h3>

        <div class="actions">
          <button
            @click="setStatus('Shortlisted')"

            :disabled="saving || info.status === 'Shortlisted'"

            class="sbtn green"
          >
            Shortlist

          </button>

          <button
            @click="setStatus('Waitlisted')"
            :disabled="saving || info.status === 'Waitlisted'"
            class="sbtn blue"
          >
            ⏳ Waitlist
          </button>
          <button
            @click="setStatus('Rejected')"

            :disabled="saving || info.status === 'Rejected'"

            class="sbtn red"
          >
             Reject
          </button>
        </div>

        <!-- msg -->

        <div v-if="msg" :class="['msg', msgtype]">{{ msg }}</div>

        <!-- resume -->
        <div v-if="info.resume">

          <a :href="info.resume" target="_blank" class="btn rbtn">
             View Resume
          </a>
        </div>
        <div v-else class="noresume">No resume uploaded</div>

      </div>

    </div>

    <!-- toast -->
    <div v-if="toast" class="toast">{{ toast }}</div>

  </div>

</template>

<script>

import api from "@/services/api";

export default {

  name: "ReviewApplication",

  data()
   {
    return {
      loading: false,
      saving: false,

      info: {},       // application data

      msg: "",
      msgtype: "ok",

      toast: "",
    };
  },

  async mounted() {
    // login check karo pehle
    const token = localStorage.getItem("token");

    const role  = localStorage.getItem("role");

    if (!token || (role !== "company" && role !== "admin")) {
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
        const res  = await api.get(`/admin/application/${id}`);

        this.info  = res.data;
      } 
      catch (e) 
      {

        this.showToast(e.response?.data?.msg || "Could not load application");
      }
      
      finally {

        this.loading = false;
      }
    },

    async setStatus(val) {
      // user se confirm karo

      const yes = confirm(`Are you sure you want to ${val.toLowerCase()} this application?`);

      if (!yes) return;

      this.saving = true;
      this.msg    = "";
      const id    = this.$route.params.appId;


      try {

        await api.post(`/company/application/${id}/status`, { status: val });

        this.info.status = val;
        this.msg  = `Status updated to "${val}" successfully!`;

        this.msgtype = "ok";
        this.showToast(`Application ${val.toLowerCase()} successfully!`);

      } catch (e) {
        this.msg     = e.response?.data?.msg || "Error updating status";

        this.msgtype = "err";
      } finally {
        this.saving = false;
      }
    },

    // badge color decide karo

    getBadge(status) {

      if (!status)
       return "";

      const s = status.toLowerCase();

      if (s === "shortlisted") 
      
      return "green";

      if (s === "rejected")   
      
      return "red";

      if (s === "waitlisted")  
      
      return "blue";

      return "yellow";

    },

    showToast(text) 
    {

      this.toast = text;
      setTimeout(() => { this.toast = ""; }, 3000);
    },

  },
};
</script>

<style scoped>

*{box-sizing: border-box; margin: 0; padding: 0;}

/* bok ka side*/
.wrap {
  min-height: 100vh;
  background: #0f172a;
  color: white;

  font-family: 'Inter', sans-serif;
  padding-bottom: 40px

}


.loader {
  position: fixed;
  inset: 0;

  background: rgba(15,23,42,0.7);
  display: flex;
  align-items: center; 

  justify-content: center;
  z-index: 9999

}



/* top ko design*/
.topbar {
  background: #1e293b;
  border-bottom: 1px solid #334155;
  padding: 18px 40px;
  display: flex;

  align-items: center; 
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
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
  align-items: center; 
  justify-content: center;

  font-size: 18px;
  cursor: pointer;
  transition: background 0.2s

}
.back:hover { background: #475569; }
/* tags ki style*/
.tag {
  font-size: 11px;
  color: #64748b;

  text-transform: uppercase;
  letter-spacing: 0.05em;
}

h1 
{
   font-size: 20px;

font-weight: 700; 
}

.right {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* extra h ye to ab*/
.badge {
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 12px; font-weight: 700;
}

.badge.green  { 
  background: #052e16; 
  color: #86efac; 
  }

.badge.yellow 
{ background: #422006;
 color: #fde68a;
  }
.badge.red   
 { background: #450a0a; 
 
 color: #fca5a5; }


.badge.blue   { background: #1e3a5f; color: #93c5fd; }


.body {
  padding: 28px 40px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 760px

}

.card {
  background: #1e293b;
  border: 1px solid #334155;

  border-radius: 16px;
  padding: 24px;
}

.stop {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;

  padding-bottom: 20px;
  border-bottom: 1px solid #334155;
}

.avatar {
  width: 56px; height: 56px;

  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  color: white;
  font-size: 24px; font-weight: 700;

  border-radius: 50%;
  display: flex;
  align-items: center; 
  justify-content: center;
  flex-shrink: 0
}

.sname  
{ 
  font-size: 20px; 
  font-weight: 700; 
  color: #e2e8f0;
  
  }

.semail 
{ font-size: 13px; 

color: #64748b; margin-top: 2px; 

}
.sdept  { 
  font-size: 13px; 
  
  color: #94a3b8; 
  margin-top: 2px; }


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
/* skilla ka*/
.skills { margin-top: 4px

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


.card h3 {
  font-size: 15px; font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 16px;
}

.actions {
  display: flex;

  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 14px;

}

.sbtn {
  padding: 10px 22px;
  border: none;

  border-radius: 9px;
  font-size: 14px; 
  font-weight: 600;

  cursor: pointer;
  transition: all 0.2s
}
.sbtn:disabled { opacity: 0.4; cursor: not-allowed; }

.sbtn.green { background: #052e16; 
color: #86efac;

border: 1px solid #166534
 }

.sbtn.green:hover:not(:disabled) {
   background: #16a34a; 
   color: white; 
   }

.sbtn.blue { background: #1e3a5f; 
color: #93c5fd;
 border: 1px solid #1d4ed8; 
 
 }

.sbtn.blue:hover:not(:disabled) { background: #1d4ed8; 
color: white

 }

.sbtn.red { background: #450a0a; 

color: #fca5a5; 
border: 1px solid #991b1b

}
.sbtn.red:hover:not(:disabled) {
  background: #dc2626; 
  color: white; }

/* msh ka design h ye */
.msg {
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px; font-weight: 500;

  margin-bottom: 14px
}

.msg.ok  { 
  background: #052e16; 

  color: #86efac; 
  border: 1px solid #166534; 

  }

.msg.err {
   background: #450a0a; 
   color: #fca5a5; 
   
   border: 1px solid #991b1b; }

.noresume {
  font-size: 13px;
  color: #475569;
  font-style: italic;
  margin-top: 4px;
}

.btn {
  padding: 9px 18px;
  border-radius: 8px;

  border: none;
  font-size: 13px; font-weight: 600;
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

.outline:hover 
{ background: rgba(96,165,250,0.1);

}

.rbtn { background: #1d4ed8; 

color: white; 
}

.rbtn:hover { 
  background: #2563eb;
   }


.toast {
  position: fixed;
  bottom: 28px; left: 50%;

  transform: translateX(-50%);
  background: #1e293b;
  border: 1px solid #334155;

  color: #e2e8f0;
  padding: 12px 24px;
  border-radius: 10px;

  font-size: 14px; font-weight: 500;
  z-index: 9000;
  box-shadow: 0 4px 20px rgba(0,0,0,0.4)

}





</style>