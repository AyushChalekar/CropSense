import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';

// Lazy load views
const Dashboard = () => import('../views/Dashboard.vue');
const Prediction = () => import('../views/Prediction.vue');
const Login = () => import('../views/LoginView.vue');
const Signup = () => import('../views/SignupView.vue');

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { title: 'CropSense - Dashboard' }
  },
  {
    path: '/predict',
    name: 'Prediction',
    component: Prediction,
    meta: { title: 'CropSense - Predict Yield' }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { title: 'CropSense - Sign In' }
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup,
    meta: { title: 'CropSense - Create Account' }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  // Fixes the "staying at the bottom" issue when changing pages
  scrollBehavior() {
    return { top: 0 };
  }
});

// Update document title based on meta
router.beforeEach((to) => {
  document.title = (to.meta.title as string) || 'CropSense';
});

export default router;