import { defineBoot } from '#q-app/wrappers'
import { createPinia } from 'pinia'
import { useRouter } from 'vue-router'

export default defineBoot(({ app }) => {
  const pinia = createPinia()
  
  // Add router to all stores
  pinia.use(({ store }) => {
    store.router = useRouter()
  })
  
  app.use(pinia)
})
