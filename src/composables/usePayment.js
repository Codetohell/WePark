// WePark/testing/frontend/src/composables/usePayment.js

import { ref } from 'vue'

/**
 * Payment Composable
 * Handles payment processing for parking reservations
 */
export function usePayment() {
    const isProcessing = ref(false)
    const error = ref(null)
    const lastPayment = ref(null)

    /**
     * Process mock payment
     */
    const processMockPayment = async (amount, reservationId) => {
        isProcessing.value = true
        error.value = null

        try {
            // Generate mock payment ID
            const mockPaymentId = `MOCK_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`

            const response = await fetch('/api/payment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({
                    payment_id: mockPaymentId,
                    amount: amount,
                    reservation_id: reservationId,
                    payment_type: 'mock'
                })
            })

            const data = await response.json()

            if (response.ok) {
                lastPayment.value = data
                return {
                    success: true,
                    paymentId: mockPaymentId,
                    data
                }
            } else {
                error.value = data.message || 'Payment processing failed'
                return { success: false, error: error.value }
            }
        } catch (err) {
            error.value = err.message || 'Payment processing failed'
            return { success: false, error: error.value }
        } finally {
            isProcessing.value = false
        }
    }

    /**
     * Process Razorpay payment
     */
    const processRazorpayPayment = async (paymentData) => {
        isProcessing.value = true
        error.value = null

        try {
            const response = await fetch('/api/payment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({
                    payment_id: paymentData.razorpayPaymentId,
                    razorpay_order_id: paymentData.razorpayOrderId,
                    razorpay_signature: paymentData.razorpaySignature,
                    amount: paymentData.amount,
                    reservation_id: paymentData.reservationId,
                    payment_type: 'razorpay'
                })
            })

            const data = await response.json()

            if (response.ok) {
                lastPayment.value = data
                return {
                    success: true,
                    data
                }
            } else {
                error.value = data.message || 'Payment processing failed'
                return { success: false, error: error.value }
            }
        } catch (err) {
            error.value = err.message || 'Payment processing failed'
            return { success: false, error: error.value }
        } finally {
            isProcessing.value = false
        }
    }

    /**
     * Verify payment
     */
    const verifyPayment = async (paymentId) => {
        isProcessing.value = true
        error.value = null

        try {
            const response = await fetch(`/api/payment?payment_id=${paymentId}`, {
                credentials: 'include'
            })
            const data = await response.json()
            return {
                success: true,
                verified: data.verified,
                data
            }
        } catch (err) {
            error.value = err.message || 'Payment verification failed'
            return { success: false, error: error.value }
        } finally {
            isProcessing.value = false
        }
    }

    /**
     * Calculate parking fee
     */
    const calculateFee = (durationHours, hourlyRate) => {
        const billingHours = Math.ceil(durationHours) // Round up
        const totalAmount = billingHours * hourlyRate
        return {
            durationHours: Math.round(durationHours * 100) / 100,
            billingHours,
            hourlyRate,
            totalAmount: Math.round(totalAmount * 100) / 100
        }
    }

    /**
     * Format currency
     */
    const formatCurrency = (amount) => {
        return `₹${amount.toFixed(2)}`
    }

    /**
     * Generate mock payment ID
     */
    const generateMockPaymentId = () => {
        return `MOCK_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    }

    /**
     * Open Razorpay checkout (placeholder)
     */
    const openRazorpayCheckout = (options) => {
        // This would integrate with actual Razorpay SDK
        console.log('Razorpay checkout:', options)
        // For now, return mock success
        return Promise.resolve({
            razorpay_payment_id: 'pay_mock_' + Date.now(),
            razorpay_order_id: options.order_id,
            razorpay_signature: 'mock_signature'
        })
    }

    return {
        // State
        isProcessing,
        error,
        lastPayment,

        // Methods
        processMockPayment,
        processRazorpayPayment,
        verifyPayment,
        calculateFee,
        formatCurrency,
        generateMockPaymentId,
        openRazorpayCheckout
    }
}
