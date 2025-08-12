<template>
  <div class="todo-list">
    <div class="row justify-between q-mb-md">
      <div class="text-h6">My Tasks</div>
      <div>
        <q-btn-group flat>
          <q-btn :color="filter === 'all' ? 'primary' : 'grey'" label="All" @click="setFilter('all')" />
          <q-btn :color="filter === 'active' ? 'primary' : 'grey'" label="Active" @click="setFilter('active')" />
          <q-btn :color="filter === 'completed' ? 'primary' : 'grey'" label="Completed" @click="setFilter('completed')" />
        </q-btn-group>
      </div>
    </div>

    <!-- Add New Todo Form -->
    <q-card class="q-mb-md">
      <q-card-section>
        <div class="text-subtitle2">Add New Task</div>
        <q-form @submit.prevent="addTodo">
          <q-input v-model="newTodo.title" label="Title" :rules="[val => !!val || 'Title is required']" />
          <q-input v-model="newTodo.description" label="Description (optional)" type="textarea" class="q-mt-sm" />
          <q-input v-model="newTodo.due_date" label="Due Date (optional)" type="date" class="q-mt-sm" />
          <div class="row justify-end q-mt-md">
            <q-btn type="submit" color="primary" label="Add Task" />
          </div>
        </q-form>
      </q-card-section>
    </q-card>

    <!-- Todo List -->
    <div class="todo-list-container">
      <div v-if="loading" class="text-center q-pa-md">
        <q-spinner color="primary" size="3em" />
        <div class="q-mt-sm">Loading tasks...</div>
      </div>

      <div v-else-if="filteredTodos.length === 0" class="text-center q-pa-md">
        <q-icon name="check_circle" size="3em" color="grey" />
        <div class="q-mt-sm text-grey">No tasks found</div>
      </div>

      <q-list v-else bordered separator class="rounded-borders">
        <todo-item 
          v-for="todo in filteredTodos" 
          :key="todo.entity_id" 
          :todo="todo" 
          @todo-updated="refreshTodos"
          @todo-deleted="refreshTodos"
        />
      </q-list>
    </div>

    <div class="row justify-between q-mt-md text-grey">
      <div>{{ activeTodoCount }} active tasks</div>
      <div>{{ completedTodoCount }} completed tasks</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useTodoStore } from '@/stores/todo'
import TodoItem from '@/components/TodoItem.vue'

const todoStore = useTodoStore()

// Local state for new todo form
const newTodo = ref({
  title: '',
  description: '',
  due_date: ''
})

// Computed properties from the store
const loading = computed(() => todoStore.loading)
const filteredTodos = computed(() => todoStore.filteredTodos)
const filter = computed(() => todoStore.filter)
const activeTodoCount = computed(() => todoStore.activeTodoCount)
const completedTodoCount = computed(() => todoStore.completedTodoCount)

// Fetch todos on component mount
onMounted(async () => {
  await todoStore.fetchTodos()
})

// Watch for filter changes and refetch todos
watch(() => todoStore.filter, async () => {
  await todoStore.fetchTodos()
})

// Methods
async function addTodo() {
  if (!newTodo.value.title.trim()) return

  const todoData = {
    title: newTodo.value.title.trim(),
    description: newTodo.value.description.trim() || null
  }

  if (newTodo.value.due_date) {
    todoData.due_date = new Date(newTodo.value.due_date).toISOString()
  }

  const success = await todoStore.createTodo(todoData)
  if (success) {
    // Reset form
    newTodo.value = {
      title: '',
      description: '',
      due_date: ''
    }
  }
}

function setFilter(filterValue) {
  todoStore.setFilter(filterValue)
}

async function refreshTodos() {
  await todoStore.fetchTodos()
}
</script>

<style lang="scss" scoped>
.todo-list-container {
  margin-bottom: 20px;
}
</style>