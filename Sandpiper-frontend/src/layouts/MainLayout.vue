<template>
  <q-layout view="lHh Lpr lFf">
    <app-header v-if="authStore.isAuthenticated" />
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import AppHeader from '@/components/AppHeader.vue'
import { useAuthStore } from 'stores/auth'
const authStore = useAuthStore()
</script>