<template>
  <q-header elevated>
    <q-toolbar>
      <q-btn
        flat
        dense
        round
        icon="menu"
        aria-label="Menu"
        @click="toggleLeftDrawer"
        v-if="authStore.isAuthenticated"
      />

      <q-toolbar-title> Sandpiper </q-toolbar-title>

      <div class="q-mr-md text-caption text-grey-5">v{{ version }}</div>

      <div v-if="authStore.isAuthenticated" class="cursor-pointer">
        Logged in as
        <b>{{ authStore.user.first_name }} {{ authStore.user.last_name }}</b>
        <q-icon size="xs" name="arrow_drop_down" />
        <q-menu anchor="bottom right" self="top right">
          <q-list style="min-width: 150px">
            <q-item clickable v-close-popup to="/profile">
              <q-item-section avatar>
                <q-icon name="person" />
              </q-item-section>
              <q-item-section>Profile</q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable v-close-popup @click="authStore.logout()">
              <q-item-section avatar>
                <q-icon name="logout" />
              </q-item-section>
              <q-item-section>Logout</q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </div>
    </q-toolbar>
  </q-header>

  <q-drawer v-if="authStore.isAuthenticated" v-model="leftDrawerOpen" show-if-above bordered>
    <q-list>
      <EssentialLink v-for="link in linksList" :key="link.title" v-bind="link" />
    </q-list>
  </q-drawer>
</template>


<script setup>
import { ref } from 'vue'
import { useAuthStore } from 'stores/auth'
import versionData from '@/version.json'
import EssentialLink from 'components/EssentialLink.vue'

const linksList = [
  {
    title: 'Dashboard',
    icon: 'dashboard',
    link: '/dashboard',
  },
  {
    title: 'Todo List',
    icon: 'check_circle',
    link: '/todos',
  },
  {
    title: 'Profile',
    icon: 'person',
    link: '/profile',
  },
]

const authStore = useAuthStore()
const version = versionData.version

const leftDrawerOpen = ref(false)

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
</script>