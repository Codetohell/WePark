<template>
  <div class="payment-overlay" @click.self="$emit('close')">
    <div class="payment-modal">
      <div class="payment-header">
        <div class="header-content">
          <div class="company-info">
            <div class="company-logo">WP</div>
            <div>
              <h3>WePark</h3>
              <p class="merchant-text">Secure Payment</p>
            </div>
          </div>
          <button class="close-btn" @click="$emit('close')" type="button">×</button>
        </div>
      </div>

      <div class="payment-body">
        <div class="amount-section">
          <div class="amount-label">Amount to Pay</div>
          <div class="amount-value">₹{{ (amount / 100).toFixed(2) }}</div>
          <div class="amount-description">{{ description }}</div>
        </div>

        <form @submit.prevent="processPayment" class="payment-form">
          <div class="form-group">
            <label>Card Number</label>
            <input
              v-model="cardNumber"
              @input="formatCardNumber"
              type="text"
              placeholder="1234 5678 9012 3456"
              maxlength="19"
              required
              class="form-input"
            />
            <div class="card-icons">
              <span class="card-icon">💳</span>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Expiry Date</label>
              <input
                v-model="expiryDate"
                @input="formatExpiry"
                type="text"
                placeholder="MM/YY"
                maxlength="5"
                required
                class="form-input"
              />
            </div>
            <div class="form-group">
              <label>CVV</label>
              <input
                v-model="cvv"
                type="text"
                placeholder="123"
                maxlength="3"
                required
                class="form-input"
              />
            </div>
          </div>

          <div class="form-group">
            <label>Cardholder Name</label>
            <input
              v-model="cardholderName"
              type="text"
              placeholder="JOHN DOE"
              required
              class="form-input"
              style="text-transform: uppercase"
            />
          </div>

          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>

          <button
            type="submit"
            class="pay-button"
            :disabled="processing"
          >
            <span v-if="!processing">Pay ₹{{ (amount / 100).toFixed(2) }}</span>
            <span v-else class="processing">
              <span class="spinner"></span>
              Processing...
            </span>
          </button>
        </form>

        <div class="security-info">
          <span class="lock-icon">🔒</span>
          <span>Secured by WePark Payment Gateway</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  amount: {
    type: Number,
    required: true
  },
  description: {
    type: String,
    default: 'Parking Fee'
  },
  onSuccess: {
    type: Function,
    required: true
  },
  onFailure: {
    type: Function,
    default: () => {}
  }
})

const emit = defineEmits(['close'])

const cardNumber = ref('')
const expiryDate = ref('')
const cvv = ref('')
const cardholderName = ref('')
const processing = ref(false)
const errorMessage = ref('')

const formatCardNumber = (e) => {
  let value = e.target.value.replace(/\s/g, '')
  let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value
  cardNumber.value = formattedValue
}

const formatExpiry = (e) => {
  let value = e.target.value.replace(/\D/g, '')
  if (value.length >= 2) {
    value = value.slice(0, 2) + '/' + value.slice(2, 4)
  }
  expiryDate.value = value
}

const processPayment = async () => {
  errorMessage.value = ''
  processing.value = true

  // Validate card number (simple check)
  const cardDigits = cardNumber.value.replace(/\s/g, '')
  if (cardDigits.length !== 16) {
    errorMessage.value = 'Invalid card number'
    processing.value = false
    return
  }

  // Validate expiry
  if (!expiryDate.value.match(/^\d{2}\/\d{2}$/)) {
    errorMessage.value = 'Invalid expiry date'
    processing.value = false
    return
  }

  // Validate CVV
  if (cvv.value.length !== 3) {
    errorMessage.value = 'Invalid CVV'
    processing.value = false
    return
  }

  // Simulate payment processing
  await new Promise(resolve => setTimeout(resolve, 2000))

  // Check for test failure card
  if (cardDigits.endsWith('1112')) {
    errorMessage.value = 'Payment failed. Please try another card.'
    processing.value = false
    props.onFailure({
      error: {
        description: 'Card declined'
      }
    })
    return
  }

  // Success
  processing.value = false
  
  // Generate mock payment response
  const mockResponse = {
    mock_payment_id: 'MOCK_pay_' + Date.now(),
    mock_order_id: 'MOCK_order_' + Date.now(),
    mock_signature: 'MOCK_sig_' + Math.random().toString(36).substr(2, 9)
  }

  props.onSuccess(mockResponse)
  emit('close')
}
</script>

<style scoped>
.payment-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.payment-modal {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 450px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease;
  overflow: hidden;
}

@keyframes slideUp {
  from {
    transform: translateY(50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.payment-header {
  background: linear-gradient(135deg, #DC143C 0%, #FF4D6D 100%);
  color: white;
  padding: 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.company-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.company-logo {
  width: 48px;
  height: 48px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 18px;
  backdrop-filter: blur(10px);
}

.company-info h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.merchant-text {
  margin: 0;
  font-size: 12px;
  opacity: 0.9;
}

.close-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  font-size: 28px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
  line-height: 1;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.payment-body {
  padding: 24px;
}

.amount-section {
  text-align: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  margin-bottom: 24px;
}

.amount-label {
  font-size: 13px;
  color: #6c757d;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.amount-value {
  font-size: 36px;
  font-weight: bold;
  color: #DC143C;
  margin-bottom: 4px;
}

.amount-description {
  font-size: 14px;
  color: #6c757d;
}

.payment-form {
  margin-top: 20px;
}

.form-group {
  margin-bottom: 16px;
  position: relative;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #495057;
}

.form-input {
  width: 100%;
  padding: 12px 14px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 15px;
  transition: all 0.2s;
  font-family: inherit;
}

.form-input:focus {
  outline: none;
  border-color: #DC143C;
  box-shadow: 0 0 0 3px rgba(220, 20, 60, 0.1);
}

.card-icons {
  position: absolute;
  right: 12px;
  top: 38px;
  font-size: 20px;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 12px;
  border-radius: 8px;
  font-size: 14px;
  margin-bottom: 16px;
  border-left: 4px solid #c33;
}

.pay-button {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #DC143C 0%, #FF4D6D 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  margin-top: 8px;
}

.pay-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(220, 20, 60, 0.3);
}

.pay-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.processing {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.security-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e9ecef;
  font-size: 13px;
  color: #6c757d;
}

.lock-icon {
  font-size: 16px;
}

@media (max-width: 480px) {
  .payment-modal {
    width: 95%;
    margin: 10px;
  }

  .amount-value {
    font-size: 28px;
  }
}
</style>
