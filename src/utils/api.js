/**
 * API utilities for making HTTP requests
 */

const BASE_URL = "/api";

/**
 * Make an API call to the backend
 * @param {string} endpoint - API endpoint (without /api prefix)
 * @param {string} method - HTTP method (GET, POST, PUT, DELETE, etc.)
 * @param {object} data - Request body data
 * @returns {Promise<{ok: boolean, status: number, resData: any}>}
 */
export async function callApi(endpoint, method = "GET", data = null) {
    try {
        const options = {
            method: method,
            headers: { "Content-Type": "application/json" },
            credentials: "include"
        };

        if (data && ["POST", "PUT", "PATCH"].includes(method)) {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(`${BASE_URL}/${endpoint}`, options);
        let resData;
        const contentType = response.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
            resData = await response.json();
        } else {
            resData = { message: "Server returned non-JSON response", raw: await response.text() };
        }

        return {
            ok: response.ok,
            status: response.status,
            resData: resData
        };

    } catch (error) {
        console.error("API call failed:", error);
        return {
            ok: false,
            status: 500,
            resData: { error: error.message || "Something went wrong!" }
        };
    }
}
