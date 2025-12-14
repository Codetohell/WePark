import { dataStore } from '../store/data';
import { getCookie, decodeToken } from '../utils';

/**
 * Authentication guard for routes
 * Checks if user is authenticated and has the correct role
 */
export function authGuard(to, from, next) {
    const data_store = dataStore();
    let role = data_store.role;

    // If no role in store, check cookie
    if (!role) {
        const token = getCookie("access_token_cookie");
        if (token) {
            const decoded = decodeToken(token);
            if (decoded) {
                data_store.updateRole(decoded.role);
                data_store.updateUsername(decoded.sub);
                data_store.updateID(decoded.id);
                role = decoded.role;
            }
        }
    }

    if (to.meta.requireAuth) {
        if (role) {
            if (to.meta.role && to.meta.role !== role) {
                // Role mismatch - redirect to appropriate dashboard
                if (role === 'admin') {
                    next('/dashboard/admin-summary');
                } else {
                    next('/dashboard/user-summary');
                }
            } else {
                next();
            }
        } else {
            // Not authenticated - redirect to login
            next('/login');
        }
    } else {
        next();
    }
}
