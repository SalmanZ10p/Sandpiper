<template>
  <div class="todo-item-wrapper">
    <q-expansion-item
      :class="{ 'completed-todo': todo.is_completed }"
      expand-separator
      :header-class="todo.is_completed ? 'text-strike' : ''"
    >
      <template v-slot:header-right>
        <div class="row items-center q-gutter-sm header-controls">
          <q-checkbox 
            v-model="isCompleted" 
            class="q-mr-md" 
            color="primary"
            size="sm"
            @click.stop
          />
          <q-btn 
            flat 
            round 
            dense 
            icon="delete" 
            color="negative" 
            size="sm"
            @click.stop="confirmDelete"
            class="delete-btn"
          />
        </div>
      </template>
      
      <!-- Fallback controls below header if header-right doesn't work -->
      <template v-slot:header>
        <div class="row items-center full-width">
          <div class="col-grow">
            <div class="text-subtitle1">{{ todo.title }}</div>
            <div v-if="todo.description" class="text-caption text-grey">{{ todo.description }}</div>
          </div>
          <div class="row items-center q-gutter-sm fallback-controls">
            <q-checkbox 
              v-model="isCompleted" 
              class="q-mr-md" 
              color="primary"
              size="sm"
              @click.stop
            />
            <q-btn 
              flat 
              round 
              dense 
              icon="delete" 
              color="negative" 
              size="sm"
              @click.stop="confirmDelete"
              class="delete-btn"
            />
          </div>
        </div>
      </template>

    <q-card>
      <q-card-section>
        <q-form @submit.prevent="saveEdit">
          <q-input
            v-model="editedTitle"
            label="Title"
            :rules="[val => !!val || 'Title is required']"
            class="q-mb-md"
          />
          
          <q-input
            v-model="editedDescription"
            label="Description"
            type="textarea"
            class="q-mb-md"
          />
          
          <q-input
            v-model="editedDueDate"
            label="Due Date"
            type="date"
            class="q-mb-md"
          />
          
          <div class="row justify-end q-gutter-sm">
            <q-btn label="Save Changes" type="submit" color="primary" />
          </div>
        </q-form>
      </q-card-section>
      
      <q-card-section v-if="todo.due_date" class="text-caption">
        Due: {{ formatDate(todo.due_date) }}
      </q-card-section>
    </q-card>
  </q-expansion-item>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { useTodoStore } from '@/stores/todo'

const props = defineProps({
  todo: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['todo-updated', 'todo-deleted'])

const $q = useQuasar()
const todoStore = useTodoStore()

// Form data
const editedTitle = ref('')
const editedDescription = ref('')
const editedDueDate = ref('')

// Initialize form data when component is mounted
onMounted(() => {
  resetForm()
})

// Computed property for checkbox
const isCompleted = computed({
  get: () => props.todo.is_completed,
  set: async (value) => {
    if (value !== props.todo.is_completed) {
      await toggleCompletion()
    }
  }
})

// Format date for display
function formatDate(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

// Reset form to current todo values
function resetForm() {
  editedTitle.value = props.todo.title || ''
  editedDescription.value = props.todo.description || ''
  
  if (props.todo.due_date) {
    const date = new Date(props.todo.due_date)
    editedDueDate.value = date.toISOString().split('T')[0]
  } else {
    editedDueDate.value = ''
  }
}

// Save edited todo
async function saveEdit() {
  if (!editedTitle.value.trim()) {
    $q.notify({
      message: 'Title cannot be empty',
      color: 'negative',
      position: 'top',
      timeout: 3000
    })
    return
  }

  const todoData = {
    title: editedTitle.value.trim(),
    description: editedDescription.value.trim() || null
  }

  if (editedDueDate.value) {
    todoData.due_date = new Date(editedDueDate.value).toISOString()
  }

  console.log('Saving todo:', todoData)
  const success = await todoStore.updateTodo(props.todo.entity_id, todoData)
  
  if (success) {
    $q.notify({
      message: 'Todo updated successfully',
      color: 'positive',
      position: 'top',
      timeout: 2000
    })
    emit('todo-updated')
  }
}

// Toggle todo completion status
async function toggleCompletion() {
  console.log('Toggle completion called for todo:', props.todo.entity_id)
  try {
    const success = await todoStore.toggleTodoCompletion(props.todo.entity_id)
    if (success) {
      emit('todo-updated')
    }
  } catch (error) {
    console.error('Error toggling completion:', error)
  }
}

// Delete todo with confirmation
async function confirmDelete(event) {
  console.log('Delete button clicked for todo:', props.todo.entity_id)
  // Prevent expansion when clicking delete
  event.stopPropagation()
  
  try {
    // Use native confirm for better compatibility
    const confirmed = confirm(`Are you sure you want to delete "${props.todo.title}"?`)
    
    if (confirmed) {
      const success = await todoStore.deleteTodo(props.todo.entity_id)
      if (success) {
        $q.notify({
          message: 'Todo deleted successfully',
          color: 'positive',
          position: 'top',
          timeout: 2000
        })
        emit('todo-deleted')
      }
    }
  } catch (error) {
    console.error('Error deleting todo:', error)
  }
}
</script>

<style lang="scss" scoped>
.todo-item-wrapper {
  position: relative;
  margin-bottom: 8px;
}

.completed-todo {
  opacity: 0.7;
}

.text-strike {
  text-decoration: line-through;
}

.header-controls {
  min-width: 80px;
  justify-content: flex-end;
  z-index: 10;
}

.delete-btn {
  margin-left: 8px;
}

// Ensure the expansion item header has enough space for controls
:deep(.q-expansion-item__header) {
  padding-right: 16px;
  min-height: 60px;
}

:deep(.q-expansion-item__header-content) {
  flex: 1;
  min-width: 0;
}

// Make sure controls are always visible
:deep(.q-expansion-item__header-right) {
  display: flex !important;
  align-items: center;
  min-width: 80px;
}

.fallback-controls {
  background: rgba(255, 255, 255, 0.9);
  padding: 4px 8px;
  border-radius: 4px;
  border: 1px solid #e0e0e0;
}
</style>