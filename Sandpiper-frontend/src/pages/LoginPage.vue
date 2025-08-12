<template>
  <q-page class="flex row flex-center">
    <q-card class="col-11 col-sm-8 col-md-6 col-lg-4 col-xl-3 q-pa-xs q-pa-md-sm q-mb-xl">
      <q-card-section>
        <div class="text-h6 text-center">Welcome to Sandpiper</div>
      </q-card-section>

      <q-card-section>
        <q-form @submit.prevent="onSubmit" class="full-width">
          <!-- Email -->
          <q-input v-model="email" type="email" label="Email" outlined class="q-mb-lg" />

          <!-- Password -->
          <q-input
            v-model="password"
            type="password"
            label="Password"
            aria-autocomplete="current-password"
            outlined
            class="q-mb-md"
          />

          <!-- Forgot Password Link -->
          <div class="text-right q-mb-md">
            <router-link to="/forgot-password">Forgot Password?</router-link>
          </div>

          <!-- Login Button -->
          <q-btn label="Login" color="primary" type="submit" class="full-width" />

          <!-- Signup Link -->
          <div class="text-center q-mt-md">
            <span>Don’t have an account? </span>
            <router-link to="/signup">Sign up</router-link>
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </q-page>
</template>
  
<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const email = ref('')
const password = ref('')

// Handle login form submission
async function onSubmit() {
  await authStore.login({ email: email.value, password: password.value })
}
</script>
  