<template>
  <div class="home-page">

    <nav class="navbar">

      <div class="nav-brand">
        
        <!-- portal ka naam -->
        <span class="brand-name">PlacementPortal</span>
      </div>

      <div class="nav-links">
        <router-link to="/login" class="nav-btn btn-outline">Login</router-link>
        <router-link to="/register" class="nav-btn btn-filled">Register</router-link>
      </div>

    </nav>


    <section class="hero-section">

      <div class="hero-content">

        <div class="hero-badge"> Campus Placement Portal V2</div>

        <h1 class="hero-title">Your Gateway to <span class="grad-text">Dream Career</span></h1>

        <!-- subttle thoda lamba hai but theek hai -->

        <p class="hero-sub">Connect talented student with top company. Apply for drives,  placements, and build your future — all in one place.</p>

        <div class="hero-btns">

          <router-link to="/register?role=student" class="cta-btn cta-blue">Get Started as Student</router-link>
          <router-link to="/register?role=company" class="cta-btn cta-white">Register Company</router-link>
        </div>


        <!-- stats section neeche -->
        <div class="stats-row">

          <div class="stat-item">
            <span class="stat-num">500+</span>
            <span class="stat-lbl">Students Placed</span>
          </div>

          <div class="stat-div"></div>

          <div class="stat-item">
            <span class="stat-num">120+</span>
            <span class="stat-lbl">Companies</span>
          </div>

          <div class="stat-div"></div>

          <div class="stat-item">
            <span class="stat-num">300+</span>
            <span class="stat-lbl">Drives Conducted</span>
          </div>

        </div>

      </div>


      <!-- right side floating cards wala part -->
      <div class="hero-visual">
        <div class="card-stack">

          <div class="float-card card-1">
           
            <div class="fc-txt">
              <span class="fc-title">SDE Drive Open</span>
              <span class="fc-sub">TechCorp • 12 LPA</span>
            </div>
          </div>

          <div class="float-card card-2">
            
            <div class="fc-txt">
              <span class="fc-title">Application Shortlisted!</span>

              <span class="fc-sub">Congratulations, User</span>
            </div>
          </div>

          <!-- 3rd card -->
          <div class="float-card card-3">
            <div class="fc-icon"></div>
            <div class="fc-txt">
              <span class="fc-title">InnovateTech Approved

              </span>
              <span class="fc-sub">New company onboarded</span>
            </div>
          </div>

        </div>
      </div>

    </section>


    <!-- kese kam krega section -->
    <section class="feat-section">

      <h2 class="sec-title">How It Works</h2>

      <div class="feat-grid">
        <div class="feat-card" v-for="f in featList" :key="f.title">
          <div class="f-icon">{{ f.icon }}</div>

          <h3>{{ f.title }}

          </h3>
          <p>{{ f.desc }}</p>
        </div>
      </div>

    </section>


    <section class="roles-sec">

      <!-- stu wala card -->

      <div class="role-card student-card">
        <h3> For Students</h3>
        <ul>
          <li>Browse verified company drives</li>
          <li>Apply with one click</li>

          <li>Track appliction status</li>
          <li>View interview & offer history</li>
        </ul>
        <router-link to="/register?role=student" class="role-btn">Join as Student →</router-link>
      </div>

      <!-- company wala card -->
      <div class="role-card company-card">
        <h3> For Companies</h3>
        <ul>
          <li>Post placement drives</li>
          <li>Review student applications</li>

          <li>Shortlist / reject candidates</li>
          <li>Manage drive lifecycle</li>
        </ul>
        <router-link to="/register?role=company" class="role-btn">Join as Company →</router-link>
      </div>

    </section>


    <footer class="footer">
      <p>© 2025 PlacementPortal V2 · Modern Application Development II</p>
    </footer>

  </div>
</template>


<script>

export default {

  name: "Home",

  data() {

    // features list jo how it works me dikhani hai
    
    return {

      featList: [
        {
         
          title: "Register",
          desc: "Students and companies register with their details. Companies await admin approval before accessing the portal."
        },

        {
          
          title: "Post Drives",
          // admin approve karega tabhi dikhai dega students ko

          desc: "Approved companies post placement drives with job details, salary, and eligibility. Admin reviews before publishing."
        },

        {
         
          title: "Apply & Track",
          desc: "Students browse open drives, apply instntly, and track their application status in real-time."
        },

        {
          
          title: "Get Placed",

          desc: "Companies shortlist candidats, conduct interviews, and finalize placemants — all managed through the portal."
        },

      ]

    };
  }

};
</script>


<style scoped>

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.home-page {
  min-height: 100vh;
  background: #f8fafc;
  font-family: 'Inter', -apple-system, sans-serif;
}


/* navbar sticky rehta hai upar */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 60px;

  background: white;
  border-bottom: 1px solid #e2e8f0;

  position: sticky;
  top: 0;
  z-index: 100;

  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 10px;

  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
}

.brand-icon { font-size: 24px }

.nav-links {
  display: flex;
  gap: 12px
}

.nav-btn {
  padding: 8px 20px;
  border-radius: 8px;

  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-outline {
  border: 1.5px solid #3b82f6;
  color: #3b82f6;
  background: transparent;
}

.btn-outline:hover { background: #eff6ff 

}

.btn-filled {
  background: #3b82f6;
  color: white;
  border: 1.5px solid #3b82f6;
}

.btn-filled:hover { background: #2563eb ;
}


/* hero section - main landing area */
.hero-section {
  display: flex;
  align-items: center;

  justify-content: space-between;

  padding: 80px 60px;
  gap: 60px;
  min-height: 90vh;

  background: linear-gradient(135deg, #f0f4ff 0%, #fafbff 100%);
}

.hero-content {
  flex: 1;
  max-width: 560px
}

.hero-badge {
  display: inline-block;
  background: #eff6ff;
  color: #3b82f6;

  border: 1px solid #bfdbfe;
  padding: 6px 16px;
  border-radius: 20px;

  font-size: 13px;
  font-weight: 600;
  margin-bottom: 24px
}

.hero-title {
  font-size: 52px;
  font-weight: 800;
  line-height: 1.15;

  color: #0f172a;
  margin-bottom: 20px
}

/* gradient wala text dream career ke liye */
.grad-text {
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;

  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-sub {
  font-size: 18px;
  color: #64748b;

  line-height: 1.65;

  margin-bottom: 36px
}

.hero-btns {
  display: flex;
  gap: 16px;
  margin-bottom: 48px;
  flex-wrap: wrap;
}

.cta-btn {
  padding: 14px 28px;
  border-radius: 10px;

  font-size: 15px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s
}

/* blue primary button */
.cta-blue {
  background: #3b82f6;
  color: white;
  box-shadow: 0 4px 14px rgba(59, 130, 246, 0.35)
}

.cta-blue:hover {
  background: #2563eb;
  transform: translateY(-1px)
}

.cta-white {
  background: white;
  color: #1e293b;
  border: 1.5px solid #e2e8f0
}

.cta-white:hover {
  border-color: #3b82f6;
  color: #3b82f6
}


.stats-row {
  display: flex;
  align-items: center;
  gap: 24px
}

.stat-item { text-align: center }

.stat-num {
  display: block;
  font-size: 28px;
  font-weight: 800;
  color: #1e293b
}

.stat-lbl {
  font-size: 12px;
  color: #64748b;
  font-weight: 500
}

/* divider line stats ke beech */
.stat-div {
  width: 1px;
  height: 40px;
  background: #e2e8f0
}


.hero-visual {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  min-height: 400px
}

.card-stack {
  position: relative;
  width: 320px;
  height: 360px
}

/* floating cards common style */
.float-card {
  position: absolute;
  background: white;
  border-radius: 14px;

  padding: 16px 20px;
  display: flex;
  align-items: center;
  gap: 14px;

  box-shadow: 0 8px 24px rgba(0,0,0,0.10);
  border: 1px solid #f1f5f9;
  width: 280px
}

.fc-icon { font-size: 28px }

.fc-txt {
  display: flex;
  flex-direction: column;
  gap: 3px
}

.fc-title {
  font-size: 14px;
  font-weight: 700;
  color: #1e293b
}

.fc-sub { font-size: 12px; color: #64748b }

/* cards ki position aur animation */
.card-1 { top: 0; left: 0; 
 }
.card-2 { top: 120px; right: 0; 

}
.card-3 { bottom: 0; left: 30px; 
 }




/* how it works wala section */
.feat-section {
  padding: 80px 60px;
  background: white;
}

.sec-title {
  font-size: 36px;
  font-weight: 800;
  color: #0f172a;

  text-align: center;
  margin-bottom: 48px
}

.feat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));

  gap: 28px;
  max-width: 1100px;
  margin: 0 auto;
}

.feat-card {
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 16px;

  padding: 32px 24px;
  transition: all 0.2s;
}

.feat-card:hover {
  border-color: #3b82f6;

  box-shadow: 0 8px 24px rgba(59,130,246,0.08);
  transform: translateY(-3px)
}

.f-icon {
  font-size: 36px;
  margin-bottom: 16px
}

.feat-card h3 {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 10px
}

.feat-card p {
  font-size: 14px;
  color: #64748b;
  line-height: 1.65
}


/* dark background roles section -->  */
.roles-sec {
  display: flex;
  gap: 28px;

  padding: 80px 60px;
  background: linear-gradient(135deg, #1e293b, #0f172a)
}

.role-card {
  flex: 1;
  background: rgba(255,255,255,0.05);

  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 20px;
  padding: 40px;

  color: white
}

.role-card h3 {
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 24px
}

.role-card ul {
  list-style: none;

  margin-bottom: 32px
}

.role-card ul li {
  padding: 8px 0;

  border-bottom: 1px solid rgba(255,255,255,0.08);

  font-size: 14px;
  color: #94a3b8;

  display: flex;
  align-items: center;
  gap: 8px;

}



.role-btn {
  display: inline-block;
  padding: 12px 24px;

  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;

}

.student-card .role-btn { background: #3b82f6;
 color: white }
.student-card .role-btn:hover 
{ background: #2563eb
 }

.company-card .role-btn { background: #8b5cf6; 

color: white }
.company-card .role-btn:hover { background: #7c3aed ;
}


.footer {
  text-align: center;
  padding: 24px;

  background: #0f172a;
  color: #475569;
  font-size: 13px;
}


/* responsive - mobile pe sab stack ho jaye */


  

  .roles-sec {
    flex-direction: column;

    padding: 50px 30px;
  }

  .navbar { 
    padding: 16px 24px;
   }

  .feat-section { padding: 60px 30px ;
  }



</style>