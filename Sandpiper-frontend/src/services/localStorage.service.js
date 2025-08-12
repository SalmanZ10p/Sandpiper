// services/localStorage.service.js
class LocalStorageService {
  /**
   * Get item from localStorage
   * @param {string} key - The key to retrieve
   * @returns {any} - Parsed value or null
   */
  getItem(key) {
    try {
      const item = localStorage.getItem(key)
      if (item === null) return null

      // Try to parse as JSON, if it fails return as string
      try {
        return JSON.parse(item)
      } catch {
        return item
      }
    } catch (error) {
      console.error(`Error getting item from localStorage: ${key}`, error)
      return null
    }
  }

  /**
   * Set item in localStorage
   * @param {string} key - The key to set
   * @param {any} value - The value to store
   */
  setItem(key, value) {
    try {
      const stringValue = typeof value === 'string' ? value : JSON.stringify(value)
      localStorage.setItem(key, stringValue)
    } catch (error) {
      console.error(`Error setting item in localStorage: ${key}`, error)
    }
  }

  /**
   * Remove item from localStorage
   * @param {string} key - The key to remove
   */
  removeItem(key) {
    try {
      localStorage.removeItem(key)
    } catch (error) {
      console.error(`Error removing item from localStorage: ${key}`, error)
    }
  }

  /**
   * Clear all items from localStorage
   */
  clear() {
    try {
      localStorage.clear()
    } catch (error) {
      console.error('Error clearing localStorage', error)
    }
  }

  /**
   * Check if localStorage is available
   * @returns {boolean}
   */
  isAvailable() {
    try {
      const test = '__localStorage_test__'
      localStorage.setItem(test, 'test')
      localStorage.removeItem(test)
      return true
    } catch {
      return false
    }
  }
}

export default new LocalStorageService()
