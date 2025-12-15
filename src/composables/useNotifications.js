// WePark/testing/frontend/src/composables/useNotifications.js

import { ref, computed } from 'vue'

/**
 * Notifications Composable
 * Handles user notifications and alerts
 */
export function useNotifications() {
    const notifications = ref([])
    const unreadNotifications = ref([])
    const isLoading = ref(false)
    const error = ref(null)

    // Computed
    const unreadCount = computed(() => unreadNotifications.value.length)
    const hasUnread = computed(() => unreadCount.value > 0)
    const notificationCount = computed(() => notifications.value.length)

    /**
     * Fetch all notifications
     */
    const fetchNotifications = async () => {
        isLoading.value = true
        error.value = null

        try {
            const response = await fetch('/api/notification', {
                credentials: 'include'
            })
            const data = await response.json()
            notifications.value = data
            return { success: true, data }
        } catch (err) {
            error.value = err.message || 'Failed to fetch notifications'
            return { success: false, error: error.value }
        } finally {
            isLoading.value = false
        }
    }

    /**
     * Fetch unread notifications only
     */
    const fetchUnreadNotifications = async () => {
        isLoading.value = true
        error.value = null

        try {
            const response = await fetch('/api/notification?unread=true', {
                credentials: 'include'
            })
            const data = await response.json()
            unreadNotifications.value = data
            return { success: true, data }
        } catch (err) {
            error.value = err.message || 'Failed to fetch unread notifications'
            return { success: false, error: error.value }
        } finally {
            isLoading.value = false
        }
    }

    /**
     * Mark notification as read
     */
    const markAsRead = async (notificationId) => {
        isLoading.value = true
        error.value = null

        try {
            const response = await fetch('/api/notification', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({
                    notification_id: notificationId
                })
            })

            const data = await response.json()

            if (response.ok) {
                await fetchUnreadNotifications() // Refresh unread count
                return { success: true, message: data.message }
            } else {
                error.value = data.message || 'Failed to mark as read'
                return { success: false, error: error.value }
            }
        } catch (err) {
            error.value = err.message || 'Failed to mark as read'
            return { success: false, error: error.value }
        } finally {
            isLoading.value = false
        }
    }

    /**
     * Mark all notifications as read
     */
    const markAllAsRead = async () => {
        isLoading.value = true
        error.value = null

        try {
            const response = await fetch('/api/notification', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({
                    mark_all: true
                })
            })

            const data = await response.json()

            if (response.ok) {
                unreadNotifications.value = []
                await fetchNotifications() // Refresh all notifications
                return { success: true, message: data.message }
            } else {
                error.value = data.message || 'Failed to mark all as read'
                return { success: false, error: error.value }
            }
        } catch (err) {
            error.value = err.message || 'Failed to mark all as read'
            return { success: false, error: error.value }
        } finally {
            isLoading.value = false
        }
    }

    /**
     * Delete notification
     */
    const deleteNotification = async (notificationId) => {
        isLoading.value = true
        error.value = null

        try {
            const response = await fetch(`/api/notification/${notificationId}`, {
                method: 'DELETE',
                credentials: 'include'
            })

            const data = await response.json()

            if (response.ok) {
                await fetchNotifications() // Refresh list
                return { success: true, message: data.message }
            } else {
                error.value = data.message || 'Failed to delete notification'
                return { success: false, error: error.value }
            }
        } catch (err) {
            error.value = err.message || 'Failed to delete notification'
            return { success: false, error: error.value }
        } finally {
            isLoading.value = false
        }
    }

    /**
     * Format notification time
     */
    const formatTime = (timestamp) => {
        const date = new Date(timestamp)
        const now = new Date()
        const diffMs = now - date
        const diffMins = Math.floor(diffMs / 60000)
        const diffHours = Math.floor(diffMs / 3600000)
        const diffDays = Math.floor(diffMs / 86400000)

        if (diffMins < 1) return 'Just now'
        if (diffMins < 60) return `${diffMins}m ago`
        if (diffHours < 24) return `${diffHours}h ago`
        if (diffDays < 7) return `${diffDays}d ago`

        return date.toLocaleDateString()
    }

    /**
     * Get notification icon based on content
     */
    const getNotificationIcon = (message) => {
        if (message.toLowerCase().includes('book')) return '🅿️'
        if (message.toLowerCase().includes('payment')) return '💳'
        if (message.toLowerCase().includes('release')) return '✅'
        if (message.toLowerCase().includes('cancel')) return '❌'
        return '🔔'
    }

    return {
        // State
        notifications,
        unreadNotifications,
        isLoading,
        error,

        // Computed
        unreadCount,
        hasUnread,
        notificationCount,

        // Methods
        fetchNotifications,
        fetchUnreadNotifications,
        markAsRead,
        markAllAsRead,
        deleteNotification,
        formatTime,
        getNotificationIcon
    }
}
