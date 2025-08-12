# Sandpiper - Todo Application

Sandpiper is a modern, full-stack todo application built with Vue.js and Flask. It provides a clean, intuitive interface for managing tasks with robust user authentication and data persistence.

![Sandpiper Logo](https://img.shields.io/badge/Sandpiper-Todo%20App-blue)
![Vue.js](https://img.shields.io/badge/Vue.js-3.x-brightgreen)
![Flask](https://img.shields.io/badge/Flask-Python-blue)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)

## Features

- **User Authentication**
  - Sign up with email
  - Login/logout functionality
  - Password reset via email
  - Edit user profile

- **Todo Management**
  - Create, read, update, and delete tasks
  - Mark tasks as complete/incomplete
  - Add task descriptions and due dates
  - Filter tasks by status (all, active, completed)

- **Modern UI**
  - Responsive design using Quasar Framework
  - Clean, intuitive interface
  - Real-time updates

- **Secure Backend**
  - RESTful API with Flask
  - PostgreSQL database
  - JWT authentication
  - Data validation

## Architecture

Sandpiper follows a modern microservices architecture:

- **Frontend**: Vue.js 3 with Quasar Framework
- **Backend**: Flask with RESTful API
- **Database**: PostgreSQL
- **Message Queue**: RabbitMQ for email notifications
- **Email Service**: Mailjet integration
- **Containerization**: Docker and Docker Compose

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js (v18+)
- npm or yarn

### Setup and Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/sandpiper.git
cd sandpiper
```

2. **Backend Setup**

```bash
cd Sandpiper-backend
# Create .env.secrets file with necessary credentials
# The .env.secrets.example file shows required variables

# Start the backend services
sudo ./run.sh
```

3. **Frontend Setup**

```bash
cd Sandpiper-frontend
npm install
npx quasar dev
```

The application will be available at http://localhost:9001 (or another port if 9001 is in use).

## Security and Authentication

The application implements robust authentication and security measures:

- **Protected Routes**: All application routes (except login, signup, and password reset) require authentication
- **Automatic Redirection**: Unauthenticated users attempting to access protected routes are automatically redirected to the login page
- **JWT Authentication**: Secure token-based authentication with expiration
- **API Security**: All API endpoints that handle user data or todos require valid authentication tokens

## API Documentation

The API documentation is available via Swagger UI at:
```
http://localhost:5000/api-doc
```

This interactive documentation allows you to:
- Browse all available API endpoints
- See required parameters and response formats
- Test API endpoints directly from the browser

## Testing Flows

### User Registration and Authentication

1. **Sign Up**
   - Navigate to http://localhost:9001/signup
   - Enter your first name, last name, and email address
   - You'll receive a welcome email with a link to set your password
   - Follow the link to set your password

2. **Login**
   - Navigate to http://localhost:9001/login
   - Enter your email and password
   - You'll be redirected to the dashboard

3. **Password Reset**
   - Navigate to http://localhost:9001/login
   - Click on "Forgot Password?"
   - Enter your email address
   - You'll receive an email with a password reset link
   - Follow the link to set a new password

4. **Profile Management**
   - After logging in, click on your name in the top-right corner
   - Select "Profile" from the dropdown menu
   - Update your first name and last name
   - Click "Save Changes"

### Todo Management

1. **Creating Tasks**
   - Navigate to http://localhost:9001/todos
   - Enter a task title (required)
   - Optionally add a description and due date
   - Click "Add Task"

2. **Managing Tasks**
   - **Mark as Complete**: Click the checkbox next to a task
   - **Edit Task**: Click the edit icon, update fields, then click the check icon
   - **Delete Task**: Click the delete icon, then confirm deletion

3. **Filtering Tasks**
   - Click "All" to see all tasks
   - Click "Active" to see only incomplete tasks
   - Click "Completed" to see only completed tasks

## Integration Testing

Sandpiper includes comprehensive integration tests for all Todo CRUD operations. These tests ensure the API endpoints work correctly and maintain data integrity.

### Running Integration Tests

To run the complete integration test suite:

```bash
cd Sandpiper-backend
./run_integration_tests.sh
```

### Test Coverage

The integration tests cover all Todo API endpoints:

1. **Create Todo Test** 📝
   - Creates todos with various data combinations
   - Tests required field validation
   - Verifies proper data storage and retrieval

2. **Read Todos Test** 📖
   - Retrieves all todos for authenticated users
   - Tests filtering by status (all, active, completed)
   - Verifies individual todo retrieval by ID
   - Confirms proper access control

3. **Update Todo Test** ✏️
   - Updates todo title, description, and due date
   - Tests completion status changes
   - Verifies toggle completion functionality
   - Ensures proper validation and error handling

4. **Delete Todo Test** 🗑️
   - Deletes individual todos
   - Verifies todos are completely removed
   - Tests deletion of non-existent todos
   - Confirms proper cleanup and list updates

### Test Features

- **🔐 Authentication Testing**: Each test creates a unique user and obtains JWT tokens
- **🧪 Isolated Tests**: Tests don't interfere with each other
- **📊 Comprehensive Reporting**: Detailed success/failure reporting with emojis
- **📝 Detailed Logging**: All test runs are logged to `logs/` directory
- **⚡ Parallel Execution**: Tests run efficiently with proper error handling

### Prerequisites for Testing

Before running integration tests, ensure:

1. **Backend is Running**:
   ```bash
   cd Sandpiper-backend
   sudo ./run.sh
   ```

2. **Python Dependencies**:
   ```bash
   pip3 install requests
   ```

3. **Database is Initialized**: The backend should be fully started with database migrations applied

### Test Output

The test runner provides:
- Real-time progress with emojis and colors
- Step-by-step execution logs
- Success rate calculations
- Detailed failure analysis
- Recommendations for fixing issues

Example successful run:
```
🧪 SANDPIPER TODO API INTEGRATION TESTS 🧪
✅ PASSED: Create Todo
✅ PASSED: Read Todos  
✅ PASSED: Update Todo
✅ PASSED: Delete Todo
📊 Success Rate: 100.0%
```

## Environment Variables

### Backend (.env.secrets)

- `APP_ENV`: Application environment (local, production)
- `POSTGRES_PASSWORD`: PostgreSQL database password
- `RABBITMQ_PASSWORD`: RabbitMQ password
- `SECRET_KEY`: Flask secret key
- `SECURITY_PASSWORD_SALT`: Password salt for encryption
- `AUTH_JWT_SECRET`: Secret for JWT token generation
- `MAILJET_API_KEY`: Mailjet API key
- `MAILJET_API_SECRET`: Mailjet API secret

### Frontend (.env)

- `VITE_API_BASE_URL`: Backend API URL (default: http://localhost:5000)

## Email Services

The application uses Mailjet for sending emails such as welcome emails and password reset links.
## Acknowledgments

- Built with [Vue.js](https://vuejs.org/) and [Quasar Framework](https://quasar.dev/)
- Backend powered by [Flask](https://flask.palletsprojects.com/) and [Rococo](https://github.com/EcorRouge/rococo)
- Email services by [Mailjet](https://www.mailjet.com/)
