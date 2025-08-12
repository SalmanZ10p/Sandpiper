import { defineStore, acceptHMRUpdate } from 'pinia'
import { Notify } from 'quasar'
import axios from 'config/axios'

export const useTodoStore = defineStore('todo', {
  state: () => ({
    todos: [],
    loading: false,
    filter: 'all', // 'all', 'active', 'completed'
  }),

  getters: {
    filteredTodos: (state) => {
      switch (state.filter) {
        case 'active':
          return state.todos.filter(todo => !todo.is_completed)
        case 'completed':
          return state.todos.filter(todo => todo.is_completed)
        default:
          return state.todos
      }
    },
    
    activeTodoCount: (state) => {
      return state.todos.filter(todo => !todo.is_completed).length
    },
    
    completedTodoCount: (state) => {
      return state.todos.filter(todo => todo.is_completed).length
    }
  },

  actions: {
    /**
     * Set filter for todos
     */
    setFilter(filter) {
      this.filter = filter
    },
    
    /**
     * Show error notification
     */
    showErrorNotification(message = 'An unknown error occurred') {
      Notify.create({
        message,
        color: 'negative',
        position: 'top',
        timeout: 5000,
      })
    },

    /**
     * Handle API errors consistently
     */
    handleApiError(error, defaultMessage = 'An unknown error occurred') {
      const message = error.response?.data?.message || error.message || defaultMessage
      this.showErrorNotification(message)
      return false
    },

    /**
     * Fetch all todos from the API
     */
    async fetchTodos() {
      try {
        this.loading = true
        const response = await axios.get(`/todo?status=${this.filter}`)
        
        if (response.data?.success) {
          this.todos = response.data.todos || []
          return true
        } else {
          this.showErrorNotification(response.data?.message)
          return false
        }
      } catch (error) {
        return this.handleApiError(error, 'Failed to fetch todos')
      } finally {
        this.loading = false
      }
    },

    /**
     * Create a new todo
     */
    async createTodo(todoData) {
      try {
        this.loading = true
        const response = await axios.post('/todo', todoData)
        
        if (response.data?.success) {
          // Add the new todo to the list
          this.todos.unshift(response.data.todo)
          
          Notify.create({
            message: 'Todo created successfully',
            color: 'positive',
            position: 'top',
            timeout: 3000,
          })
          
          return true
        } else {
          this.showErrorNotification(response.data?.message)
          return false
        }
      } catch (error) {
        return this.handleApiError(error, 'Failed to create todo')
      } finally {
        this.loading = false
      }
    },

    /**
     * Update an existing todo
     */
    async updateTodo(todoId, todoData) {
      console.log('Store updateTodo called with:', todoId, todoData)
      try {
        this.loading = true
        console.log('Making API call to PUT /todo/' + todoId)
        const response = await axios.put(`/todo/${todoId}`, todoData)
        console.log('API response:', response.data)
        
        if (response.data?.success) {
          // Update the todo in the list
          const index = this.todos.findIndex(t => t.entity_id === todoId)
          if (index !== -1) {
            this.todos[index] = response.data.todo
          }
          
          Notify.create({
            message: 'Todo updated successfully',
            color: 'positive',
            position: 'top',
            timeout: 3000,
          })
          
          return true
        } else {
          this.showErrorNotification(response.data?.message)
          return false
        }
      } catch (error) {
        console.error('Update todo error:', error)
        return this.handleApiError(error, 'Failed to update todo')
      } finally {
        this.loading = false
      }
    },

    /**
     * Delete a todo
     */
    async deleteTodo(todoId) {
      try {
        this.loading = true
        const response = await axios.delete(`/todo/${todoId}`)
        
        if (response.data?.success) {
          // Remove the todo from the list
          this.todos = this.todos.filter(t => t.entity_id !== todoId)
          
          Notify.create({
            message: 'Todo deleted successfully',
            color: 'positive',
            position: 'top',
            timeout: 3000,
          })
          
          return true
        } else {
          this.showErrorNotification(response.data?.message)
          return false
        }
      } catch (error) {
        return this.handleApiError(error, 'Failed to delete todo')
      } finally {
        this.loading = false
      }
    },

    /**
     * Toggle the completion status of a todo
     */
    async toggleTodoCompletion(todoId) {
      try {
        this.loading = true
        const response = await axios.put(`/todo/${todoId}/toggle`)
        
        if (response.data?.success) {
          // Update the todo in the list
          const index = this.todos.findIndex(t => t.entity_id === todoId)
          if (index !== -1) {
            this.todos[index] = response.data.todo
          }
          
          return true
        } else {
          this.showErrorNotification(response.data?.message || 'Failed to toggle todo')
          return false
        }
      } catch (error) {
        console.error('Toggle completion error:', error)
        this.showErrorNotification('Failed to toggle todo completion')
        return false
      } finally {
        this.loading = false
      }
    }
  }
})

// Hot Module Replacement support
if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useTodoStore, import.meta.hot))
}
