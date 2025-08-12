<template>
  <q-page padding>
    <div class="row justify-center">
      <div class="col-12 col-md-8 col-lg-6">
        <q-card class="q-pa-md">
          <q-card-section>
            <div class="text-h6">Edit Profile</div>
          </q-card-section>

          <q-card-section>
            <q-form @submit.prevent="updateProfile">
              <q-input
                v-model="profileData.first_name"
                label="First Name"
                :rules="[val => !!val || 'First name is required']"
                class="q-mb-md"
              />

              <q-input
                v-model="profileData.last_name"
                label="Last Name"
                :rules="[val => !!val || 'Last name is required']"
                class="q-mb-md"
              />

              <q-input
                v-model="profileData.email"
                label="Email"
                type="email"
                readonly
                class="q-mb-md"
              />

              <div class="row justify-end q-mt-md">
                <q-btn
                  type="submit"
                  color="primary"
                  label="Save Changes"
                  :loading="loading"
                />
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { Notify } from 'quasar'
import axios from 'config/axios'

const authStore = useAuthStore()
const loading = ref(false)

const profileData = ref({
  first_name: '',
  last_name: '',
  email: ''
})

onMounted(() => {
  // Initialize form with current user data
  if (authStore.user) {
    profileData.value = {
      first_name: authStore.user.first_name || '',
      last_name: authStore.user.last_name || '',
      email: authStore.user.email || ''
    }
  }
})

async function updateProfile() {
  if (!profileData.value.first_name || !profileData.value.last_name) {
    Notify.create({
      message: 'Please fill in all required fields',
      color: 'negative',
      position: 'top',
      timeout: 3000
    })
    return
  }

  try {
    loading.value = true
    const response = await axios.put('/person/me', {
      first_name: profileData.value.first_name,
      last_name: profileData.value.last_name
    })

    if (response.data?.success) {
      // Update the user data in the auth store
      authStore.updateUser({
        first_name: profileData.value.first_name,
        last_name: profileData.value.last_name
      })

      Notify.create({
        message: 'Profile updated successfully',
        color: 'positive',
        position: 'top',
        timeout: 3000
      })
    } else {
      Notify.create({
        message: response.data?.message || 'Failed to update profile',
        color: 'negative',
        position: 'top',
        timeout: 3000
      })
    }
  } catch (error) {
    const message = error.response?.data?.message || error.message || 'An unknown error occurred'
    Notify.create({
      message,
      color: 'negative',
      position: 'top',
      timeout: 5000
    })
  } finally {
    loading.value = false
  }
}
</script>
