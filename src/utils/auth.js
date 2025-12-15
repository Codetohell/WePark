import { dataStore } from "../store/data";
import { getCookie } from "./cookies";
import { decodeToken } from "./jwt";

/**
 * Authentication utilities
 */

/**
 * Check if user is authenticated and update store
 * @returns {boolean} True if authenticated, false otherwise
 */
export const tokenChecker = () => {
    const token = getCookie("access_token_cookie");
    if (!token) {
        return false;
    }

    const decoded = decodeToken(token);
    if (!decoded) {
        return false;
    }

    const store = dataStore();
    store.updateRole(decoded.role);
    store.updateUsername(decoded.sub);
    store.updateID(decoded.id);

    return true;
};
