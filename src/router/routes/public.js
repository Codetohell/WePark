/**
 * Public routes - accessible without authentication
 */

const Home = () => import('@/views/Home.vue');
const Login = () => import('@/views/Login.vue');
const Signup = () => import('@/views/Signup.vue');

export const publicRoutes = [
    {
        path: '/',
        component: Home,
        meta: {
            requireAuth: false
        }
    },
    {
        path: '/login',
        component: Login,
        meta: {
            requireAuth: false
        }
    },
    {
        path: '/signup',
        component: Signup,
        meta: {
            requireAuth: false
        }
    }
];
