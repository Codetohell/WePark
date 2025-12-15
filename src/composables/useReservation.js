// WePark/testing/frontend/src/composables/useReservation.js

import { ref, computed } from 'vue'

/**
 * Reservation Composable
 * Handles parking spot booking and reservation management
 */
export function useReservation() {
    const reservations = ref([])
    const activeReservations = ref([])
    const isLoading = ref(false)
    const error = ref(null)

    // Computed
    const hasReservations = computed(() => reservations.value.length > 0)
    const hasActiveReservations = computed(() => activeReservations.value.length > 0)
    const reservationCount = computed(() => reservations.value.length)

    /**
     * Book a parking spot
     */
    const bookSpot = async (spotId) => {
        isLoading.value = true
        error.value = null

        try {
            const response = await fetch('/api/spot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({
                    spot_id: spotId
                })
            })

            const data = await response.json()

            if (response.ok) {
                await fetchActiveReservations() // Refresh active reservations
                return { success: true, message: data.message }
            } else {
                error.value = data.message || 'Failed to book spot'
                return { success: false, error: error.value }
            }
        } catch (err) {
            error.value = err.message || 'Failed to book spot'
            return { success: false, error: error.value }
        } finally {
            isLoading.value = false
        }
    }

    /**
     * Release a parking spot (complete reservation)
     */
    const releaseSpot = async (reservationId, paymentId = null) => {
        isLoading.value = true
        error.value = null

        try {
            const response = await fetch('/api/reservation', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({
                    reservation_id: reservationId,
                    payment_id: paymentId
                })
            })

            const data = await response.json()

            if (response.ok) {
                await fetchActiveReservations() // Refresh active reservations
                return {
                    success: true,
                    message: data.message,
                    totalAmount: data.total_amount
                }
            } else {
                error.value = data.message || 'Failed to release spot'
                return { success: false, error: error.value }
            }
        } catch (err) {
            error.value = err.message || 'Failed to release spot'
            return { success: false, error: error.value }
        } finally {
            isLoading.value = false
        }
    }

    /**
     * Fetch all reservations for current user
     */
    const fetchReservations = async () => {
        isLoading.value = true
        error.value = null

        try {
            const response = await fetch('/api/reservation', {
                credentials: 'include'
            })
            const data = await response.json()
            reservations.value = data
            return { success: true, data }
        } catch (err) {
            error.value = err.message || 'Failed to fetch reservations'
            return { success: false, error: error.value }
        } finally {
            isLoading.value = false
        }
    }

    /**
     * Fetch active reservations only
     */
    const fetchActiveReservations = async () => {
        isLoading.value = true
        error.value = null

        try {
            const response = await fetch('/api/reservation?active=true', {
                credentials: 'include'
            })
            const data = await response.json()
            activeReservations.value = data
            return { success: true, data }
        } catch (err) {
            error.value = err.message || 'Failed to fetch active reservations'
            return { success: false, error: error.value }
        } finally {
            isLoading.value = false
        }
    }

    /**
     * Calculate parking duration in hours
     */
    const calculateDuration = (startTime, endTime = null) => {
        const start = new Date(startTime)
        const end = endTime ? new Date(endTime) : new Date()
        const durationMs = end - start
        const durationHours = durationMs / (1000 * 60 * 60)
        return Math.round(durationHours * 100) / 100 // Round to 2 decimals
    }

    /**
     * Calculate parking cost
     */
    const calculateCost = (startTime, pricePerHour, endTime = null) => {
        const duration = calculateDuration(startTime, endTime)
        const billingHours = Math.ceil(duration) // Round up
        return billingHours * pricePerHour
    }

    /**
     * Format reservation status
     */
    const getStatusLabel = (status) => {
        const labels = {
            'active': 'Active',
            'completed': 'Completed',
            'cancelled': 'Cancelled'
        }
        return labels[status] || status
    }

    /**
     * Get status color class
     */
    const getStatusColor = (status) => {
        const colors = {
            'active': 'success',
            'completed': 'info',
            'cancelled': 'danger'
        }
        return colors[status] || 'secondary'
    }

    return {
        // State
        reservations,
        activeReservations,
        isLoading,
        error,

        // Computed
        hasReservations,
        hasActiveReservations,
        reservationCount,

        // Methods
        bookSpot,
        releaseSpot,
        fetchReservations,
        fetchActiveReservations,
        calculateDuration,
        calculateCost,
        getStatusLabel,
        getStatusColor
    }
}
