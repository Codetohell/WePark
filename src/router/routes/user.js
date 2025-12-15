/**
 * User routes - require user role
 */

const UserSummary = () => import('@/views/Summary/User.vue');
const AvailableLots = () => import('@/views/AvailableLots.vue');
const ParkingHistory = () => import('@/views/ParkingHistory.vue');
const Notification = () => import('@/views/Notification.vue');

export const userRoutes = [
    {
        path: 'user-summary',
        component: UserSummary,
        meta: {
            requireAuth: true,
            role: 'user'
        }
    },
    {
        path: 'available_lots',
        component: AvailableLots,
        meta: {
            requireAuth: true,
            role: 'user'
        }
    },
    {
        path: 'parking-history',
        component: ParkingHistory,
        meta: {
            requireAuth: true,
            role: 'user'
        }
    },
    {
        path: 'notification',
        component: Notification,
        meta: {
            requireAuth: true,
            role: 'user'
        }
    }
];
