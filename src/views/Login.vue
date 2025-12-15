<style>
/* Global background and animation for animated cars, matching Signup.vue */
:root {
  --aerospace: #DC143C;
  --silver: #B2B2B2;
  --calamansi: #E4FEA3;
  --orange: #FF4D6D;
  --tan: #FF8FA3;
  --white: #FFFFFF;
  --bg: #0d0706;
  --card: #151010;
  --muted: rgba(255, 255, 255, .65);
  --border: rgba(255, 255, 255, .08);
  --glass: rgba(255, 255, 255, .06);
}

body {
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans", "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", sans-serif;
  background: url('/src/assets/colorful_cars_bg.png');
  background-size: 300px;
  background-repeat: repeat;
  background-color: #0a0808;
  color: var(--white);
  overflow-x: hidden;
  animation: traffic-move 10s ease-in-out infinite;
}

@keyframes traffic-move {
  0% { background-position: 0 0; }
  50% { background-position: 0 30px; }
  100% { background-position: 0 0; }
}
</style>
<template>
  <div class="screen">
    <section class="login-section">
      <div class="login-container glossy-card">
        <div class="row align-items-stretch g-0">
          <!-- Left Art -->
          <div class="col-lg-6">
            <div class="art-wrap">
              <img class="art-img floaty" src="/src/assets/login.png" alt="mascot illustration" />
            </div>
          </div>
          <!-- Right Form -->
          <div class="col-lg-6 form-column">
            <div class="form-wrap">
              <h2 class="login-title">Sign In to WePark</h2>
              <form @submit.prevent="handleLogin">
                <div class="mb-3">
                  <label class="form-label">Username or Email</label>
                  <div class="input-shell">
                    <span class="left-ico">
                      <!-- User Icon -->
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                        <circle cx="12" cy="6" r="4" stroke="#fff" stroke-width="1.7" />
                        <path d="M15 20.615C14.0907 20.8619 13.0736 21 12 21c-1.0736 0-2.0907-.1381-3-.3849M14 21v-5.5c0-1.1046-.8954-2-2-2s-2 .8954-2 2V21" stroke="#fff" stroke-width="1.7" />
                      </svg>
                    </span>
                    <input v-model="credentials.userOrMail" type="text" class="form-control" placeholder="Enter username or email" required :disabled="isLoading" />
                  </div>
                </div>
                <div class="mb-3">
                  <label class="form-label">Password</label>
                  <div class="input-shell">
                    <span class="left-ico">
                      <!-- Lock Icon -->
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                        <rect x="4" y="11" width="16" height="9" rx="2.2" stroke="#fff" stroke-width="1.7" />
                        <path d="M8 11V8a4 4 0 1 1 8 0v3" stroke="#fff" stroke-width="1.7" />
                      </svg>
                    </span>
                    <input :type="showPwd ? 'text' : 'password'" v-model="credentials.password" class="form-control pe-5" placeholder="Enter password" required :disabled="isLoading" />
                    <button type="button" class="btn position-absolute end-0 top-0 h-100 px-3 border-0 bg-transparent" @click="showPwd = !showPwd" aria-label="Toggle password">
                      <svg v-if="!showPwd" width="20" height="20" viewBox="0 0 24 24" fill="none">
                        <path d="M2.5 12s3.7-6.5 9.5-6.5S21.5 12 21.5 12 17.8 18.5 12 18.5 2.5 12 2.5 12z" stroke="#fff" stroke-width="1.7" />
                        <circle cx="12" cy="12" r="3" stroke="#fff" stroke-width="1.7" />
                      </svg>
                      <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none">
                        <path d="M3 3l18 18" stroke="#fff" stroke-width="1.7" />
                        <path d="M6 6.8C3.8 8.4 2.5 12 2.5 12s3.7 6.5 9.5 6.5c1.6 0 3-.3 4.2-.8M16.5 8.2C15.2 7.6 13.7 7.5 12 7.5 6.2 7.5 2.5 12 2.5 12" stroke="#fff" stroke-width="1.7" />
                      </svg>
                    </button>
                  </div>
                </div>
                <div v-if="error" class="alert-error mt-3">
                  {{ error }}
                </div>
                <div class="mt-4 mb-2">
                  <button class="btn btn-cta w-100" type="submit" :disabled="isLoading">
                    {{ isLoading ? 'Signing in...' : 'Sign In' }}
                  </button>
                </div>
              </form>
              <div class="small muted text-center mt-3">
                Don't have an account? <router-link class="linkish" to="/signup">Sign up here</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables'

const router = useRouter()
const { login, isLoading, error } = useAuth()

const credentials = ref({
  userOrMail: '',
  password: ''
})
const showPwd = ref(false)

const handleLogin = async () => {
  try {
    const result = await login(credentials.value)
    if (result.success) {
      // Redirect based on role
      if (result.role === 'admin') {
        router.push('/dashboard/admin-summary')
      } else {
        router.push('/dashboard/user-summary')
      }
    } else if (result.message) {
      // Show error message from backend
      error.value = result.message
    } else {
      error.value = 'Login failed. Please try again.'
    }
  } catch (e) {
    error.value = 'An unexpected error occurred. Please try again.'
    // Optionally log error for debugging
    // console.error(e)
  }
}
</script>

<style scoped>
/* --- Copied and adapted from Signup.vue for consistency --- */

/* ...existing code... */

.screen {
  background: radial-gradient(100% 40% at 50% -5%, rgba(255, 255, 255, .06), transparent), rgba(10, 8, 8, .85);
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, .06), 0 40px 120px rgba(0, 0, 0, .65);
  padding: 26px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

@keyframes floaty {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-12px); }
}

.login-section {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
  position: relative;
}

.login-container {
  max-width: 1040px;
  width: 100%;
  overflow: hidden;
}

.art-wrap {
  height: 560px;
  position: relative;
  overflow: visible;
  border-right: 1px solid var(--border);
}

.art-img {
  position: absolute;
  bottom: -32px;
  left: -24px;
  width: 125%;
  max-width: none;
  z-index: 1;
  user-select: none;
  pointer-events: none;
}

.art-img.floaty {
  animation: floaty 5s ease-in-out infinite;
}

.form-column {
  padding: 40px;
  position: relative;
  z-index: 2;
}

.form-wrap {
  max-width: 400px;
  margin: 0 auto;
}

.login-title {
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 30px;
  text-align: center;
}


.form-label {
  font-weight: 600;
  color: var(--white);
  margin-bottom: 8px;
  display: block;
  font-size: 0.95rem;
}

.input-shell {
  position: relative;
}

.input-shell .left-ico {
  position: absolute;
  top: 50%;
  left: 16px;
  transform: translateY(-50%);
  color: var(--muted);
  pointer-events: none;
  opacity: 0.8;
}


.form-control {
  height: 48px;
  background: rgba(255, 255, 255, .06);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding-left: 48px;
  color: var(--white);
  font-size: 0.95rem;
  transition: all 0.3s;
}

.form-control:focus {
  border-color: var(--aerospace);
  box-shadow: 0 0 0 3px rgba(139, 92, 246, .2);
  background: rgba(255, 255, 255, .08);
  color: white;
}

.form-control::placeholder {
  color: var(--white);
  opacity: 0.8;
}

/* Match button style to Signup page */
.btn-cta.w-100 {
  height: 48px;
  font-size: 1rem;
  border-radius: 999px;
  font-weight: 700;
  background: radial-gradient(100% 120% at 30% 20%, #fff2, transparent 45%),
    linear-gradient(90deg, var(--orange), var(--aerospace));
  border: 0;
  box-shadow: 0 10px 24px rgba(139, 92, 246, .45), inset 0 1px rgba(255, 255, 255, .35);
  color: #fff;
  transition: filter 0.2s;
}

.btn-cta.w-100:hover {
  filter: brightness(1.05);
}


.alert-error {
  background: rgba(139, 92, 246, 0.2);
  border: 1px solid var(--aerospace);
  color: var(--white);
  padding: 10px 16px;
  border-radius: 12px;
  font-size: 0.9rem;
  text-align: center;
}

.muted {
  color: var(--muted);
  font-size: 0.9rem;
}

.linkish {
  color: var(--aerospace);
  text-decoration: none;
  font-weight: 600;
}

.linkish:hover {
  text-decoration: underline;
  color: var(--orange);
}

/* Glossy Card Style */
.glossy-card {
  position: relative;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, .08) 0%, rgba(255, 255, 255, .03) 28%, rgba(0, 0, 0, .50) 100%),
    radial-gradient(140% 120% at 50% -10%, rgba(167, 139, 250, .55), rgba(139, 92, 246, .15) 35%, transparent 60%),
    #130e0e;
  border: 1px solid var(--border);
  border-radius: 22px;
  box-shadow:
    inset 0 1px rgba(255, 255, 255, .25),
    inset 0 20px 60px rgba(255, 255, 255, .04),
    0 18px 40px rgba(0, 0, 0, .6),
    0 20px 60px rgba(139, 92, 246, .15);
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
}

.glossy-card::before {
  content: "";
  position: absolute;
  left: -8%;
  right: -8%;
  top: -10%;
  height: 55%;
  background: linear-gradient(to bottom, rgba(255, 255, 255, .35), rgba(255, 255, 255, 0));
  filter: blur(18px);
  pointer-events: none;
}

.glossy-card::after {
  content: "";
  position: absolute;
  inset: auto -30% -30% -30%;
  height: 55%;
  background: radial-gradient(60% 120% at 50% 0%, rgba(139, 92, 246, .25), transparent 65%);
  filter: blur(22px);
  pointer-events: none;
}

.glossy-card:hover {
  transform: translateY(-5px);
  box-shadow:
    inset 0 1px rgba(255, 255, 255, .25),
    inset 0 20px 60px rgba(255, 255, 255, .04),
    0 22px 48px rgba(0, 0, 0, .7),
    0 24px 72px rgba(139, 92, 246, .2);
}

@media (max-width: 992px) {
  .art-img {
    width: 140%;
    bottom: -30%;
  }
}

@media (max-width: 768px) {
  .art-column {
    height: 300px;
    border-right: none;
    border-bottom: 1px solid var(--border);
  }
  .form-column {
    padding: 30px 20px;
  }
  .login-title {
    font-size: 1.8rem;
  }
}
</style>