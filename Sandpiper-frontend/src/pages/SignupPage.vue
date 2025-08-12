<template>
  <q-page class="flex row flex-center">
    <q-dialog v-model="successDialog" persistent>
      <q-card>
        <q-card-section>
          <div class="text-h6">Signup successful</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          Account created successfully. Check your email for a verification link and follow the link
          to set a password for your account.
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Back to login" color="primary" @click="backToLogin" />
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-card class="col-11 col-sm-8 col-md-6 col-lg-4 col-xl-3 q-pa-xs q-pa-md-sm q-mb-xl">
      <q-card-section>
        <div class="text-h6 text-center">Create an account</div>
      </q-card-section>

      <q-card-section>
        <q-form @submit.prevent="onSubmit" class="full-width">
          <!-- First name -->
          <q-input v-model="firstName" type="text" label="First name" outlined class="q-mb-lg" />

          <!-- Last name -->
          <q-input v-model="lastName" type="text" label="Last name" outlined class="q-mb-lg" />

          <!-- E-mail address -->
          <q-input
            v-model="emailAddress"
            type="email"
            label="E-mail address"
            outlined
            class="q-mb-xl"
          />

          <!-- Signup Button -->
          <q-btn
            label="Create account"
            color="primary"
            type="submit"
            class="full-width"
            :loading="signupLoading"
          />

          <!-- Signup Link -->
          <div class="text-center q-mt-md">
            <span>Already have an account? </span>
            <router-link to="/login">Log in</router-link>
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </q-page>
</template>
    
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from 'stores/auth'

const firstName = ref('')
const lastName = ref('')
const emailAddress = ref('')

const successDialog = ref(false)
const signupLoading = ref(false)

const router = useRouter()

const authStore = useAuthStore()

// Handle signup form submission
async function onSubmit() {
  signupLoading.value = true

  let success = await authStore.signup({
    first_name: firstName.value,
    last_name: lastName.value,
    email_address: emailAddress.value,
  })

  signupLoading.value = false

  if (success) {
    successDialog.value = true
  }
}

function backToLogin() {
  router.push('/login')
}
</script>
    