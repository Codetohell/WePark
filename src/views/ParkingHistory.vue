<template>
    <div class="history-container container my-5">
      <div class="history-card p-4">
        <h3 class="mb-4 fw-bold">Parking History</h3>
        <div class="table-responsive">
          <table class="table table-borderless custom-table text-center align-middle">
            <thead>
              <tr class="mb-2">
                <th>Prime Location</th>
                <th>Spot ID</th>
                <th>Vehicle No.</th>
                <th>Parking Time</th>
                <th>Leaving Time</th>
                <th>Total Cost</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(history, index) in HistoryData" :key="index">
                <td>{{ history.prime_location }}</td>
                <td>{{ history.spot_id }}</td>
                <td>{{ history.vehicle_number }}</td>
                <td>{{ formatDate(history.parking_time) }}</td>
                <td>{{ formatDate(history.end_time) }}</td>
                <td>₹{{ formatCost(history.parking_cost) }}</td>
                <td>
                  <span class="badge bg-secondary">Parked Out</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onBeforeUnmount } from 'vue'
  import { callApi } from '@/utils.js'
  const formatDate = (datetime) => {
    if (!datetime) return '-'
    const date = new Date(datetime)
    return date.toLocaleString("en-IN", {
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      hour12: true
    })
  }
  
  const formatCost = (cost) => {
    if (!cost) return '0.00'
    // If cost is greater than 1000, it's likely stored in paise (old data)
    // Divide by 100 to convert to rupees
    const rupees = cost > 1000 ? cost / 100 : cost
    return rupees.toFixed(2)
  }
  
  const HistoryData = ref([])

  const ParkingHistory = async () => {
    try {
      const {ok, status, resData} = await callApi("reservation")
      if (ok) {
        // Filter for completed reservations (those with end_time and parking_cost)
        const completedReservations = resData.filter(r => r.end_time && r.parking_cost !== null && r.parking_cost !== undefined)
        
        // Sort by end_time (desc)
        HistoryData.value = completedReservations.sort((a, b) => {
          const aTime = new Date(a.end_time)
          const bTime = new Date(b.end_time)
          return bTime - aTime
        })
      } else {
        alert(resData?.message || "Something went wrong! ")
      }
    } catch (err) {
      console.log(err)
    }
  }

  onMounted(() => {
    ParkingHistory()
    window.addEventListener('parking-history-refresh', ParkingHistory)
  })
  onBeforeUnmount(() => {
    window.removeEventListener('parking-history-refresh', ParkingHistory)
  })
  </script>
  
  <style scoped>
  .history-card {
    background: transparent;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 1rem;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.277);
    color: var(--text-primary);
  }
  
  .custom-table {
    background-color: transparent;
  }
  
  .custom-table thead th {
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .custom-table tbody tr {
    line-height: 2.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  }
  
  .custom-table td, .custom-table th {
    background-color: transparent !important;
    color: var(--text-primary);
  }
  
  .badge {
    font-size: 0.9rem;
    padding:10px;
    border-radius: 1rem;
  }
  </style>
  