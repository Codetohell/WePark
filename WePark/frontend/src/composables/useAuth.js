// WePark/testing/frontend/src/composables/useAuth.js

import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { dataStore } from '../store/data'

/**
 * Authentication Composable
 * Handles user authentication, login, logout, and session management
 */
export function useAuth() {
    const router = useRouter()
    const store = dataStore()

    const isLoading = ref(false)
    const error = ref(null)

    // Computed properties
    const isAuthenticated = computed(() => !!store.username)
    const currentUser = computed(() => ({
        username: store.username,
        role: store.role,
        id: store.id
    }))
    const isAdmin = computed(() => store.role === 'admin')
    const isUser = computed(() => store.role === 'user')

    /**
     * Login user or admin
     */
    const login = async (credentials) => {
        isLoading.value = true
        error.value = null

        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({
                    user_or_mail: credentials.userOrMail,
                    password: credentials.password
                })
            })

            const data = await response.json()

            if (response.ok) {
                const { role, username } = data

                // Update store
                store.updateRole(role)
                store.updateUsername(username)

                return { success: true, role, username }
            } else {
                error.value = data.message || 'Login failed'
                return { success: false, error: error.value }
            }
        } catch (err) {
            error.value = err.message || 'Login failed'
            return { success: false, error: error.value }
        } finally {
            isLoading.value = false
        }
    }

    /**
     * Register new user
     */
    const signup = async (userData) => {
        isLoading.value = true
        error.value = null

        try {
            const response = await fetch('/api/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({
                    email: userData.email,
                    username: userData.username,
                    password: userData.password,
                    confirm_password: userData.confirmPassword,
                    address: userData.address,
                    pincode: userData.pincode
                })
            })

            const data = await response.json()

            if (response.ok) {
                return { success: true, message: data.message }
            } else {
                error.value = data.message || 'Signup failed'
                return { success: false, error: error.value }
            }
        } catch (err) {
            error.value = err.message || 'Signup failed'
            return { success: false, error: error.value }
        } finally {
            isLoading.value = false
        }
    }

    /**
     * Logout current user
     */
    const logout = async () => {
        isLoading.value = true
        error.value = null

        try {
            await fetch('/api/logout', {
                method: 'POST',
                credentials: 'include'
            })

            // Clear store
            store.updateRole('')
            store.updateUsername('')
            store.updateID('')

            // Redirect to home
            router.push('/')

            return { success: true }
        } catch (err) {
            error.value = err.message || 'Logout failed'
            return { success: false, error: error.value }
        } finally {
            isLoading.value = false
        }
    }

    /**
     * Check if user has specific role
     */
    const hasRole = (role) => {
        return store.role === role
    }

    /**
     * Require authentication - redirect if not authenticated
     */
    const requireAuth = () => {
        if (!isAuthenticated.value) {
            router.push('/login')
            return false
        }
        return true
    }

    /**
     * Require specific role - redirect if not authorized
     */
    const requireRole = (role) => {
        if (!requireAuth()) return false

        if (!hasRole(role)) {
            router.push('/')
            return false
        }
        return true
    }

    return {
        // State
        isLoading,
        error,

        // Computed
        isAuthenticated,
        currentUser,
        isAdmin,
        isUser,

        // Methods
        login,
        signup,
        logout,
        hasRole,
        requireAuth,
        requireRole
    }
}
