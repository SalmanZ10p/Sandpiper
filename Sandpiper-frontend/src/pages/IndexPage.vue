<template>
  <q-page class="flex flex-center column">
    <h4>Welcome to Sandpiper, {{ authStore.user?.first_name }} {{ authStore.user?.last_name }}</h4>
    <p class="q-mt-md">Manage your tasks efficiently with our Todo app.</p>
    <q-btn
      color="primary"
      label="Go to Todo List"
      icon="check_circle"
      to="/todos"
      class="q-mt-lg"
    />
  </q-page>
</template>

<script setup>
import { useAuthStore } from 'stores/auth'

const authStore = useAuthStore()
</script>
