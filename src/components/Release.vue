<template>
    <form @submit.prevent="payNow" class="book-lot-form container p-5">
      <h4 class="mb-4 fw-bold text-center">Book Parking Spot</h4>
  
      <div class="row g-4">
        <div class="col-12 d-flex align-items-center">
            <label class="me-3 fw-bold" style="min-width: 120px;">Spot ID:</label>
            <input type="text" v-model="details.spot_id" disabled class="form-control form-control-lg" />
        </div>
        <div class="col-12 d-flex align-items-center">
            <label class="me-3 fw-bold" style="min-width: 120px;">Vehicle Number:</label>
            <input type="text" v-model="details.vehicle_number" disabled class="form-control form-control-lg" />
        </div>
        <div class="col-12 d-flex align-items-center">
            <label class="me-3 fw-bold" style="min-width: 120px;">Parking Time:</label>
            <input type="text" v-model="details.parking_time" disabled class="form-control form-control-lg" />
        </div>
        <div class="col-12 d-flex align-items-center">
            <label class="me-3 fw-bold" style="min-width: 120px;">Leaving Time:</label>
            <input type="text" v-model="details.leaving_time" disabled class="form-control form-control-lg" />
        </div>
        <div class="col-12 d-flex align-items-center">
            <label class="me-3 fw-bold" style="min-width: 120px;">Total Cost:</label>
            <!-- <input type="text" :value=details.total_cost/100 disabled class="form-control form-control-lg" /> -->
            <input type="text" :value="(details.total_cost / 100).toFixed(2)" disabled class="form-control form-control-lg" />
        </div>
    </div>

        
    
  
      <div class="d-flex justify-content-end gap-3 mt-5">
        <button type="submit" class="btn btn-success btn-lg px-4">Pay & Release</button>
        <button type="button" class="btn btn-outline-secondary btn-lg px-4" @click="emit('cancel')">Cancel</button>
      </div>
    </form>

    <!-- Mock Payment Gateway Modal -->
    <MockPaymentGateway
      v-if="showPaymentModal"
      :amount="order.amount"
      :description="'Parking Fee - Spot #' + details.spot_id"
      :onSuccess="handlePaymentSuccess"
      :onFailure="handlePaymentFailure"
      @close="showPaymentModal = false"
    />

    <!-- Debug logs removed from user view -->
  </template>
  
  <script setup>
  import { onMounted, ref, watchEffect, toRefs } from 'vue'
  import { dataStore } from '@/store/data.js'
  import { callApi } from '@/utils.js'
  import { useRouter } from 'vue-router'
  import MockPaymentGateway from './MockPaymentGateway.vue'

  const store = dataStore()
  const router = useRouter()

  const emit = defineEmits(['cancel'])

  const props = defineProps({
  reservationDetail: {
    type: Object,
    required: true
  }
})
const details = ref({})
const showPaymentModal = ref(false)
const debugLogs = ref([])

const addLog = (msg) => {
  debugLogs.value.push(new Date().toLocaleTimeString() + ': ' + msg)
  console.log(msg)
}

const { reservationDetail } = toRefs(props)
watchEffect(() => {
  details.value = reservationDetail.value.reservation_data
  addLog("Details loaded: " + JSON.stringify(details.value))
})
const order = reservationDetail.value

const payNow = async () => {
  addLog("payNow called")
  if (!details.value || !details.value.reservation_id) {
    addLog("Error: Missing reservation details")
    alert("Error: Missing reservation details")
    return
  }
  addLog("Opening payment modal. Amount: " + order.amount)
  
  // Show mock payment gateway
  showPaymentModal.value = true
}

const handlePaymentSuccess = async (response) => {
  addLog("handlePaymentSuccess called")
  addLog("Payment response: " + JSON.stringify(response))
  
  try {
    const payload = {
      "reservation_id": details.value.reservation_id,
      "order_id": response.mock_order_id,
      "payment_id": response.mock_payment_id,
      "signature": response.mock_signature,
      "total_cost": details.value.total_cost,
      "amount": order.amount
    }
    
    addLog("Sending payload: " + JSON.stringify(payload))
    const {ok, resData} = await callApi("reservation", "POST", payload)
    addLog("API Response: " + ok + " " + JSON.stringify(resData))
    
    if (ok) {
      alert("Payment successful! Spot released.")
      emit('cancel')
      
      // Add delay to ensure backend processes update
      setTimeout(() => {
        router.push('/dashboard/parking-history')
      }, 500)
    } else {
      alert("Payment verification failed: " + (resData.message || "Unknown error"))
    }
  } catch (err) {
    addLog("Error: " + err.message)
    console.error("Payment verification error:", err)
    alert('Payment verification failed: ' + err.message);
  }
}

const handlePaymentFailure = (error) => {
  addLog("Payment failed: " + JSON.stringify(error))
  console.error("=== PAYMENT FAILED ===", error)
  alert('Payment failed: ' + (error.error?.description || 'Unknown error'))
}

  </script>
  
  <style scoped>
  .book-lot-form {
    background: var(--bg-modalbg);
    border-radius: 1rem;
    max-width: 720px;
    width: 100%;
    color: var(--text-modal);
  }
  .book-lot-form h4 {
    color: var(--text-modal) !important;
  }
  .book-lot-form label {
    color: var(--text-modal) !important;
  }
  .book-lot-form input,
  .book-lot-form input.form-control {
    color: #1e293b !important;
    background-color: #ffffff;
  }
  .book-lot-form input:disabled,
  .book-lot-form input.form-control:disabled {
    color: #64748b !important;
    background-color: #f1f5f9;
  }
  input::placeholder {
    font-weight: 500;
    color: #6c757d !important;
    opacity: 1;
  }
  input:focus {
    box-shadow: 0 0 0 0.2rem rgba(25, 135, 84, 0.25);
  }
  </style>
  