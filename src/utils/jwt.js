import { jwtDecode } from "jwt-decode";

/**
 * JWT token utilities
 */

/**
 * Decode a JWT token
 * @param {string} token - JWT token string
 * @returns {object|null} Decoded token payload or null if invalid
 */
export const decodeToken = (token) => {
    try {
        return jwtDecode(token);
    } catch (error) {
        console.error("Failed to decode token:", error);
        return null;
    }
};
