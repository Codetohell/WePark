/**
 * Admin routes - require admin role
 */

const AdminSummary = () => import('@/views/Summary/Admin.vue');
const Lot = () => import('@/views/Lot.vue');
const AdminUsers = () => import('@/views/AdminUsers.vue');
const Payment = () => import('@/views/Payment.vue');

export const adminRoutes = [
    {
        path: 'admin-summary',
        component: AdminSummary,
        meta: {
            requireAuth: true,
            role: 'admin'
        }
    },
    {
        path: 'lot',
        component: Lot,
        meta: {
            requireAuth: true,
            role: 'admin'
        }
    },
    {
        path: 'users',
        component: AdminUsers,
        meta: {
            requireAuth: true,
            role: 'admin'
        }
    },
    {
        path: 'payment',
        component: Payment,
        meta: {
            requireAuth: true,
            role: 'admin'
        }
    }
];
