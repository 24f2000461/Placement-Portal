import { createRouter, createWebHistory } from "vue-router";

// saare views import kr rhe h
import Home from "@/views/Home.vue";
import Login from "@/views/Login.vue";
import Registration from "@/views/Registration.vue";
import AdminDashboard from "@/views/AdminDashboard.vue";
import CompanyDashboard from "@/views/CompanyDashboard.vue";
import CreateJob from "@/views/CreateJob.vue";
import StudentDashboard from "@/views/StudentDashboard.vue";
import DriveApplications from "@/views/DriveApplications.vue";
import ReviewApplication from "@/views/ReviewApplication.vue";
import StudentApplication from "@/views/StudentApplication.vue"; // student apni application dekh skta h

const routes = [

  // home aur auth routes
  { path: "/",
    name: "Home",
    component: Home },

  { path: "/login",
    name: "Login",
    component: Login },

  { path: "/register",
    name: "Registration",
    component: Registration },

  // admin ka dashboard sirf admin dekh skta h
  { path: "/admin-dashboard",
    name: "AdminDashboard",
    component: AdminDashboard,
    meta: { role: "admin" } },

  // company ke saare routes
  { path: "/company-dashboard",
    name: "CompanyDashboard",
    component: CompanyDashboard,
    meta: { role: "company" } },

  { path: "/create-job", // naya job/drive banane ke liye
    name: "CreateJob",
    component: CreateJob,
    meta: { role: "company" } },

  {
    path: "/drive-applications/:driveId", // ek drive ke saare applicants
    name: "DriveApplications",
    component: DriveApplications,
    meta: { role: "company" }
  },

  {
    path: "/review-application/:appId", // company ek application review kregi yahan
    name: "ReviewApplication",
    component: ReviewApplication,
    meta: { role: "company" }
  },

  // student wale routes
  { path: "/student-dashboard",
    name: "StudentDashboard",
    component: StudentDashboard,
    meta: { role: "student" } },

  {
    path: "/my-application/:appId", // student apni single application ka detail
    name: "StudentApplication",
    component: StudentApplication,
    meta: { role: "student" }
  },

  

  // company interview schedule kregi is route se
  

  // company placement export - csv download
 

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// ye guard check krta h ki sahi banda sahi page pe ja rha h
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role"); // login ke time save kiya tha

  if (to.meta.role) {
    if (!token) {
      // login nhi h toh wapas bhejo
      next("/login");
      return
    }

    if (to.meta.role !== role) {
      // banda galat role ke page pe ja rha h
      // jis role ka h usi ka dashboard dikhao
      if (role === "admin") next("/admin-dashboard");
      
      else if (role === "company") next("/company-dashboard");
      else next("/student-dashboard");
    } else {
      next(); // sab sahi h jaane do
    }
  } else {
    next(); // public route h koi rok nhi
  }
});

export default router;