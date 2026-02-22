import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';

// Lazy load views for better performance
const Dashboard = () => import('../views/Dashboard.vue');
const Prediction = () => import('../views/Prediction.vue');

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
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;