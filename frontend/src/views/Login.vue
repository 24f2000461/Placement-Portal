<template>
  <div class="login-main-wrapper">


    <div class="left-wala-div">
      <div class="brand-top">
      
        <span>PlacementPortal

        </span>
      </div>

      <h2>Welcome Back!</h2>
      <p>Login to access your dashboard and manage placements.</p>

      <div class="cards-bottom-area">
        <div class="ek-card" v-for="c in cardsList" :key="c.txt">

          <span>{{ c.ic }}</span>
          <span>{{ c.txt }}</span>
        </div>
      </div>
    </div>


    <div class="right-wala-div">
      <div class="form-box">
        <h1>Login</h1>
        <p class="neeche-wali-line">Enter your credential to continue</p>
        
 <!-- login ka h ye -->
        <form @submit.prevent="handleLogin">

          <div class="field">
            <label>Email Address</label>
            <input
              v-model="formData.email_address"

              type="email"
              placeholder="your@email.com"
              required
            />
          </div>

          <div class="field">
            <label>Password</label>
            <input
              v-model="formData.password"

              type="password"
              placeholder="123"
              required
            />
          </div>

          <!-- error ya succ dono me se ek dikhega -->
          <div v-if="errText" class="msg-box err-msg">
            
            {{ errText }}</div>

          <div v-if="okText" class="msg-box ok-msg">
            
            {{ okText }}</div>

          <button type="submit" :disabled="isLoading" class="login-btn">
            <span v-if="isLoading" class="spin-loader"></span>

            {{ isLoading ? "Logging in..." : "Login" }}
          </button>

        </form>

        <p class="register-link-text">
          Don't have an account?

          <router-link to="/register">Register here</router-link>
        </p>

        <!-- demo credentils sec -->

        <div class="demo-section">
          <p class="demo-heading">Demo Credentials</p>

          <div class="demo-row" @click="fillAdminCreds">
            <span>👤 Admin</span>
            <span class="cred-text">11d@gmail.com / admin</span>
          </div>
        </div>

      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Login",

  data() {
    return {

      // form ka data yahan store hoga
      formData: {
        email_address: "",
        password: "",
      },

      errText: "",    // err msg

      okText: "",     // succ msg
      isLoading: false,

      // left side ke cards
      cardsList: [
        { ic: "", txt: "Apply to top drives" },

        { ic: "", txt: "Manage company drives" 

        },

        { ic: "", txt: "Admin oversight" 

        },
      ],
    };
  },

  methods: {

    // admin ke creds directly fill karta hai click pe
    fillAdminCreds() {
      this.formData.email_address = "11d@gmail.com";
      this.formData.password = "admin";
    },

    async handleLogin() {
      // pehle clear karo purane messages
      this.errText = "";
      this.okText = "";
      this.isLoading = true;

      try {
        const resp = await axios.post("http://127.0.0.1:5001/login", this.formData);

        this.okText = "Login successful! Redirecting...";

        // token aur baaki cheezein localStorage me daal do
        localStorage.setItem("token",    resp.data.token);

        localStorage.setItem
        ("role",     resp.data.role);
        localStorage.setItem("userId",   resp.data.user_id)
        ;
        localStorage.setItem
        ("userName", resp.data.name);

        // thoda wait karo phir redirect
        setTimeout(() => {
          const userRole = resp.data.role;

          if (userRole === "admin")       
           this.$router.push(
          { name: "AdminDashboard" }
          
          )
          ;
          else if (userRole === "company") 

          this.$router.push({ name: "CompanyDashboard" });

          else                            
          
          this.$router.push({ name: "StudentDashboard" });

        }, 800);

      } catch (err) {
        // backend se jo bhi message aaye woh dikhao

        this.errText = err.response?.data?.msg || "Server not responding. Check backend.";
      }
       finally {

        this.isLoading = false;
      }
    },
  },

  mounted()
   {
    // agar pehle se login hai toh seedha dashbord pe bhejo

    const savedToken = localStorage.getItem("token");
    const savedRole  = localStorage.getItem("role");

    if (savedToken && savedRole) 
    {

      if (savedRole === "admin")       
       this.$router.push("/admin-dashboard");

      else if (savedRole === "company") 
      
      this.$router.push("/company-dashboard");
      else                             
       this.$router.push("/student-dashboard");
    }
  },
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.login-main-wrapper {
  min-height: 100vh;
  display: flex;
  font-family: 'Inter', -apple-system, sans-serif;
}

/* ---- left side ---- */
.left-wala-div {
  flex: 1;
  background: linear-gradient(135deg,  #1e293b 0%,  #0f172a 100%);
  color: white;
  padding: 60px 50px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.brand-top {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 20px;
  font-weight: 700;
  color: #60a5fa;
}

.icon-emoji { font-size: 28px; }

.left-wala-div h2 {
  font-size: 36px;
  font-weight: 800;
  margin-top: 40px;
  line-height: 1.2;
}

.left-wala-div p {
  color: #94a3b8;
  font-size: 15px;
  line-height:   1.65;
}

.cards-bottom-area {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap:  12px;
}

.ek-card {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255,255,255, 0.10);
  border-radius: 12px;
  padding: 14px 18px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: #cbd5e1


}

/* ight side*/
.right-wala-div {
  flex: 1;
  background: #f8fafc;
  display:  flex;
  align-items: center;
  justify-content:  center;
  padding: 40px 30px;
}

.form-box {
  background: white;
  border-radius: 20px;
  padding: 44px 40px;

  width: 100%;
  max-width: 440px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0

}

.form-box h1 {
  font-size: 28px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom:  8px;
}

.neeche-wali-line {
  color: #64748b;
  font-size: 14px;
  margin-bottom: 32px;
}

/* input fields */
.field { margin-bottom: 20px; }

.field label {
  display: block;
  font-size: 13px;

  font-weight:  600;
  color: #374151;
  margin-bottom: 7px;

}

.field input {
  width: 100%;
  padding: 12px 14px;
  border: 1.5px solid  #e2e8f0;
  border-radius: 10px;
  font-size: 14px;

  color: #1e293b;
  outline:  none;
  transition: border-color 0.2s,  box-shadow 0.2s;

  background: #f8fafc;
}

.field input:focus {
  border-color: #3b82f6;

  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.12);
  background: white;
}

/* mesgs */
.msg-box {
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 13px;

  font-weight: 500;
  margin-bottom:  16px;
}

.err-msg {
  background: #fef2f2;
  color: #dc2626;

  border: 1px solid #fecaca;
}

.ok-msg {
  background: #f0fdf4;
  color:  #16a34a;
  border: 1px solid #bbf7d0;
}

/* login button */
.login-btn {
  width: 100%;
  padding:  13px;

  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 10px;

  font-size: 15px;
  font-weight: 600;
  cursor: pointer;

  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap:  8px;
  margin-top: 8px;
}

.login-btn:hover:not(:disabled)

{ background: #2563eb;

}
.login-btn:disabled { 
  opacity: 0.65;
  
  cursor: not-allowed; }



/* register link */
.register-link-text {
  text-align: center;

  margin-top:  24px;
  font-size: 14px;
  color: #64748b;
}

.register-link-text a {
  color: #3b82f6;

  font-weight: 600;
  text-decoration: none;
}

.register-link-text a:hover { text-decoration: underline; }

/* demo section */

.demo-section 
{
  margin-top: 24px;
  border-top: 1px solid  #e2e8f0;
  padding-top:  20px
}

.demo-heading {

  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;

  color: #94a3b8;
  margin-bottom:  10px;
}

.demo-row {
  display:  flex;
  justify-content: space-between;
  align-items: center;

  padding: 10px 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;

  cursor: pointer;
  transition: all 0.15s;
  font-size: 13px;

  font-weight: 500;
  color: #1e293b;
}

.demo-row:hover {
  border-color: #3b82f6;

  background: #eff6ff;
}

.cred-text {
  font-size: 11px;
  color: #64748b;
  font-family: monospace

}



</style>