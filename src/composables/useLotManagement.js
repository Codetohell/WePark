// WePark/testing/frontend/src/composables/useLotManagement.js

import { ref, computed } from 'vue'

/**
 * Lot Management Composable
 * Handles parking lot CRUD operations and search
 */
export function useLotManagement() {
    const lots = ref([])
    const currentLot = ref(null)
    const isLoading = ref(false)
    const error = ref(null)

    // Computed
    const lotsCount = computed(() => lots.value.length)
    const hasLots = computed(() => lots.value.length > 0)

    /**
     * Fetch all lots with optional filters
     */
    const fetchLots = async (filters = {}) => {
        isLoading.value = true
        error.value = null

        try {
            const params = new URLSearchParams()
            if (filters.name) params.append('name', filters.name)
            if (filters.pincode) params.append('pincode', filters.pincode)
            if (filters.address) params.append('address', filters.address)

            const url = `/api/lot${params.toString() ? '?' + params.toString() : ''}`
            const response = await fetch(url, {
                credentials: 'include'
            })

            const data = await response.json()
            lots.value = data
            return { success: true, data }
        } catch (err) {
            error.value = err.message || 'Failed to fetch lots'
            return { success: false, error: error.value }
        } finally {
            isLoading.value = false
        }
    }

    /**
     * Fetch single lot by ID
     */
    const fetchLotById = async (lotId) => {
        isLoading.value = true
        error.value = null

        try {
            const response = await fetch(`/api/lot/${lotId}`, {
                credentials: 'include'
            })

            const data = await response.json()
            currentLot.value = data
            return { success: true, data }
        } catch (err) {
            error.value = err.message || 'Failed to fetch lot'
            return { success: false, error: error.value }
        } finally {
            isLoading.value = false
        }
    }

    /**
     * Create new parking lot
     */
    const createLot = async (lotData) => {
        isLoading.value = true
        error.value = null

        try {
            const response = await fetch('/api/lot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({
                    prime_location: lotData.primeLocation,
                    price_per_hour: lotData.pricePerHour,
                    address: lotData.address,
                    pincode: lotData.pincode,
                    no_of_spots: lotData.noOfSpots
                })
            })

            const data = await response.json()

            if (response.ok) {
                await fetchLots() // Refresh list
                return { success: true, message: data.message }
            } else {
                error.value = data.message || 'Failed to create lot'
                return { success: false, error: error.value }
            }
        } catch (err) {
            error.value = err.message || 'Failed to create lot'
            return { success: false, error: error.value }
        } finally {
            isLoading.value = false
        }
    }

    /**
     * Update existing lot
     */
    const updateLot = async (lotId, lotData) => {
        isLoading.value = true
        error.value = null

        try {
            const response = await fetch(`/api/lot/${lotId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({
                    prime_location: lotData.primeLocation,
                    price_per_hour: lotData.pricePerHour,
                    address: lotData.address,
                    pincode: lotData.pincode
                })
            })

            const data = await response.json()

            if (response.ok) {
                await fetchLots() // Refresh list
                return { success: true, message: data.message }
            } else {
                error.value = data.message || 'Failed to update lot'
                return { success: false, error: error.value }
            }
        } catch (err) {
            error.value = err.message || 'Failed to update lot'
            return { success: false, error: error.value }
        } finally {
            isLoading.value = false
        }
    }

    /**
     * Delete lot
     */
    const deleteLot = async (lotId) => {
        isLoading.value = true
        error.value = null

        try {
            const response = await fetch(`/api/lot/${lotId}`, {
                method: 'DELETE',
                credentials: 'include'
            })

            const data = await response.json()

            if (response.ok) {
                await fetchLots() // Refresh list
                return { success: true, message: data.message }
            } else {
                error.value = data.message || 'Failed to delete lot'
                return { success: false, error: error.value }
            }
        } catch (err) {
            error.value = err.message || 'Failed to delete lot'
            return { success: false, error: error.value }
        } finally {
            isLoading.value = false
        }
    }

    /**
     * Search lots by query
     */
    const searchLots = async (query) => {
        return await fetchLots({ name: query })
    }

    /**
     * Get available spots for a lot
     */
    const getAvailableSpots = (lot) => {
        if (!lot || !lot.spots) return []
        return lot.spots.filter(spot => spot.status === 'available')
    }

    /**
     * Get occupied spots for a lot
     */
    const getOccupiedSpots = (lot) => {
        if (!lot || !lot.spots) return []
        return lot.spots.filter(spot => spot.status === 'occupied')
    }

    /**
     * Calculate occupancy rate
     */
    const getOccupancyRate = (lot) => {
        if (!lot || !lot.spots || lot.spots.length === 0) return 0
        const occupied = getOccupiedSpots(lot).length
        return Math.round((occupied / lot.spots.length) * 100)
    }

    return {
        // State
        lots,
        currentLot,
        isLoading,
        error,

        // Computed
        lotsCount,
        hasLots,

        // Methods
        fetchLots,
        fetchLotById,
        createLot,
        updateLot,
        deleteLot,
        searchLots,
        getAvailableSpots,
        getOccupiedSpots,
        getOccupancyRate
    }
}
