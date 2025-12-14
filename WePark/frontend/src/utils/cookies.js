/**
 * Cookie utilities
 */

/**
 * Get a cookie value by key
 * @param {string} key - Cookie name
 * @returns {string|null} Cookie value or null if not found
 */
export const getCookie = (key) => {
    const cookies = document.cookie.split("; ");
    for (const c of cookies) {
        const parts = c.split("=");
        const k = parts[0];
        if (k === key) {
            return parts.slice(1).join("=");
        }
    }
    return null;
};

/**
 * Remove a cookie by key
 * @param {string} key - Cookie name
 */
export const removeCookie = (key) => {
    document.cookie = `${key}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
};
