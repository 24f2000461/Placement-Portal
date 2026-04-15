<template>
  <div class="reg-page">

    <div class="left-side">
      <div class="top-logo">
       
       
        <span>PlacementPortal</span>
      </div>

      <h2>Join the Portal</h2>
      <p>Create your account as a student or company and start your placement journey.</p>

      <div class="bottom-role-cards">

        <div class="one-role-card student-card">
        
          <div>
            <strong>Students</strong>
            <p>Instant access after registration</p>
          </div>
        </div>

        <div class="one-role-card company-card">
         
          <div>
            <strong>Companies</strong>

            <p>Access after admin approval</p>
          </div>
        </div>

      </div>
    </div>


    <div class="right-side">
      <div class="main-form-box">

        <h1>Create Account</h1>
        <p class="small-sub-text">Fill in your details below</p>

        <form @submit.prevent="doRegister">

          <!-- name aur contact ek row me -->
          <div class="two-col-row">
            <div class="field-wrap">

              <label>Full Name *</label>
              <input v-model="regForm.name" placeholder="John Doe" required />
            </div>
            <div class="field-wrap">
              <label>Contact Number *</label>
              <input v-model="regForm.phone" placeholder="9876543210" required />
            </div>
          </div>

          <div class="field-wrap">
            <label>Email Address *</label>
            <input v-model="regForm.email_address" type="email" placeholder="your@email.com" required />
          </div>

          <div class="field-wrap">
            <label>Password *</label>
            <input v-model="regForm.password" type="password" placeholder="Min 6 characters" required />
          </div>

          <!-- gender aur role ek row me -->
          <div class="two-col-row">
            <div class="field-wrap">

              <label>Gender *</label>
              <select v-model="regForm.gender" required>
                <option value="">Select</option>

                <option value="Male">Male</option>
                <option value="Female">Female

                </option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div class="field-wrap">
              <label>Register As *</label>

              <select v-model="regForm.system_user_role" required>

                <option value="">Select Role

                </option>
                <option value="student">Student

                </option>

                <option value="company">Company</option>
              </select>
            </div>
          </div>

          <!-- company walo ko batao ki approval lagegi -->

          <div v-if="regForm.system_user_role === 'company'" class="approval-box">
             Company accounts require admin approval before login
          </div>

          <!-- msg dikhao succ ya err -->

          <div v-if="statusMsg" :class="['msg-box', isSuccess ? 'ok-msg' : 'err-msg']">
            {{ statusMsg }}
          </div>

          <button type="submit" :disabled="isBusy" class="reg-btn">
            <span v-if="isBusy" class="spin-circle"></span>
            {{ isBusy ? "Registering..." : "Create Account" }}
          </button>

        </form>

        <p class="login-link-line">
          Already have an account?
          <router-link to="/login">Login here</router-link>
        </p>

      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Registration",

  data() {
    return {

      // saara form data yahan hai
      regForm: {
        name: "",
        email_address: "",
        password: "",
        phone: "",        // contact ke liye
        gender: "",
        system_user_role: ""
      },

      statusMsg: "",     // error ya success message
      isSuccess: false,  // green dikhana hai ya red
      isBusy: false,     // button disable karne ke liye
    };
  },

  methods: {

    async doRegister() {

      // sabse pehle check karo koi field khaali toh nahi
      const f = this.regForm;
      if (!f.name || !f.email_address || !f.password || !f.phone || !f.gender || !f.system_user_role) {
        this.statusMsg = "Please fill all required fields";

        this.isSuccess = false;
        return;
      }

      this.isBusy = true;

      this.statusMsg = "";

      try {
        // backend ko data bhejo

        const result = await axios.post("http://127.0.0.1:5001/registration", this.regForm);

        this.statusMsg = result.data.message;

        this.isSuccess = true;

        // form saaf karo
        this.regForm = {

          name: "", email_address: "", password: "",
          phone: "", gender: "", system_user_role: ""
        };

        // thodi der baad login page pe bhejo
        setTimeout(() => this.$router.push("/login"), 1500);

      } catch (err) {
        // kuch gadbad hui
        this.statusMsg = err.response?.data?.message || "Registration failed";
        this.isSuccess = false;
      } finally {
        this.isBusy = false;
      }
    }
  },

  mounted() {
    // agar url me role aaya hai query se toh seedha set karo
    const roleFromUrl = this.$route.query.role;
    if (roleFromUrl === "student" || roleFromUrl === "company") {
      this.regForm.system_user_role = roleFromUrl;
    }
  }
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}

/* poora page layout */
.reg-page {
  min-height: 100vh;
  display: flex;
  font-family: 'Inter', -apple-system, sans-serif;
}

/* ---- left wala panel ---- */
.left-side {
  flex: 0.8;
  background: linear-gradient(135deg, #1e293b 0%,   #0f172a 100%);
  color: white;
  padding: 60px 50px;
  display: flex;
  flex-direction: column;
  gap:  20px;
}

.top-logo {
  display:  flex;
  align-items: center;
  gap: 10px;
  font-size: 20px;
  font-weight: 700;
  color: #60a5fa;
}

.logo-icon { font-size: 28px; }

.left-side h2 {
  font-size: 32px;
  font-weight:  800;
  margin-top: 40px;
}

.left-side p {
  color: #94a3b8;
  font-size: 14px;
  line-height: 1.65;
}

/* role cards neeche */
.bottom-role-cards {
  margin-top:  auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.one-role-card {
  display: flex;
  align-items: center;
  gap:  14px;
  padding: 16px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.student-card {
   background: rgba(59, 130, 246, 0.12); }

.company-card { 
  background: rgba(139, 92, 246,  0.12)
  }

.card-icon { font-size: 24px; }

.one-role-card strong {
  display: block;
  font-size: 14px;
  color: white;
  margin-bottom:  4px;
}

.one-role-card p
 {
  font-size: 12px;
  color: #94a3b8;

  margin: 0;
}

/* reght wala panel*/
.right-side {
  flex: 1.2;
  background:  #f8fafc;
  display: flex;

  align-items: center;
  justify-content:  center;
  padding: 40px 30px;
}

.main-form-box {
  background: white;
  border-radius: 20px;
  padding: 44px 40px;
  width: 100%;
  max-width: 520px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid  #e2e8f0;
}

.main-form-box h1 {
  font-size: 26px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom:  6px;
}

.small-sub-text {
  color: #64748b;
  font-size:  14px;
  margin-bottom: 28px;
}

/* do col wali row */
.two-col-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap:  16px;
}

.field-wrap { 
  
  margin-bottom: 18px; 
  }

.field-wrap label {
  display: block;
  font-size: 12px;

  font-weight:  700;
  color: #374151;
  margin-bottom: 6px;

  text-transform: uppercase;
  letter-spacing: 0.04em

}

.field-wrap input,

.field-wrap select {
  width: 100%;

  padding: 11px 14px;

  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  font-size:  14px;


  color: #1e293b;
  outline: none;
  transition: border-color 0.2s,  box-shadow 0.2s;
  background: #f8fafc;
  
}

.field-wrap input:focus,
.field-wrap select:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.12);
  background: white;
}

/* company approvl notice */
.approval-box {
  background: #fffbeb;
  border: 1px solid  #fbbf24;
  border-radius: 10px;
  padding: 12px 16px;

  font-size:  13px;
  color: #92400e;
  margin-bottom: 16px

}

/* msge boxes */
.msg-box {
  padding: 12px 16px;
  border-radius:  10px;
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 16px;
}

.err-msg {

  background: #fef2f2;
  color:  #dc2626;
  border: 1px solid #fecaca;
}

.ok-msg {
  background: #f0fdf4;
  color: #16a34a;
  border: 1px solid  #bbf7d0

}

/* reg btn */
.reg-btn {
  width:  100%;
  padding: 13px;
  background: #3b82f6;
  color: white;

  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight:  600;
  cursor: pointer;

  transition: all 0.2s;
  display: flex;
  align-items:  center;
  justify-content: center;

  gap: 8px;
}

.reg-btn:hover:not(:disabled) {
  
  background: #2563eb
  
  }
.reg-btn:disabled {
   opacity: 0.65; 
   
   cursor: not-allowed; }

/* loading spinner ab nhi chiye */


/* login link neeche */
.login-link-line {
  text-align:  center;

  margin-top: 20px;
  font-size: 14px;
  color: #64748b;
}

.login-link-line a {
  color:  #3b82f6;
  font-weight: 600;
  text-decoration: none

}

.login-link-line a:hover { text-decoration: underline; }

/* mobile view */

</style>