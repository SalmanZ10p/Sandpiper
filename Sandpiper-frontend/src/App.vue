<template>
  <router-view />
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// Initialize authentication when app starts
onMounted(() => {
  authStore.initialize()
})
</script>

