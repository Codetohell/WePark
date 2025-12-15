import { createRouter, createWebHistory } from 'vue-router';
import { authGuard } from './guards';
import { publicRoutes } from './routes/public';
import { adminRoutes } from './routes/admin';
import { userRoutes } from './routes/user';

const Dashboard = () => import('@/views/Dashboard.vue');

const routes = [
    ...publicRoutes,
    {
        path: '/dashboard',
        component: Dashboard,
        meta: {
            requireAuth: true
        },
        children: [
            ...adminRoutes,
            ...userRoutes
        ]
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

// Enable authentication guard for protected routes
router.beforeEach(authGuard);

export default router;