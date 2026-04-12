# TaskFlow - Real-Time Project Management Tool

TaskFlow is a robust, full-stack project management application featuring a React-based Kanban board and a high-performance FastAPI backend. It leverages Server-Sent Events (SSE) to ensure multiple users see task updates instantly, without needing to refresh their browsers.

## 🎥 Demo

![Demo Video](final.gif)

---

## 🚀 How to Run the Application

The fastest way to get everything running is by using Docker. Follow these exact copy-paste steps in your terminal to launch the application.

```bash
# 1. Clone the repository and navigate into the project directory
git clone https://github.com/Ajay9330/taskflow-ajaykumar.git
cd taskflow-ajaykumar

# 2. Copy the example environment file
cp .env.example .env

# 3. Build and start the containers in detached mode
docker-compose up -d --build
```

**That's it!** The backend container automatically handles the database migrations (`alembic upgrade head`) on startup.

Once the containers are up and healthy (usually takes 5-10 seconds), access the application here:
- **Frontend App:** [http://localhost:3000](http://localhost:3000)
- **Backend API Docs (Swagger):** [http://localhost:8080/docs](http://localhost:8080/docs)

---

## 👥 How to Test Multi-User Real-Time Updates

To see the Server-Sent Events (SSE) in action, you can test how the application handles multiple concurrent users looking at the same project board.

1. **Open Two Browser Windows:**
   - Open **Browser Window A** (e.g., Chrome).
   - Open **Browser Window B** (e.g., an Incognito window, or Firefox).

2. **Register/Login:**
   - Since the database is fresh, create a new account in Window A (e.g., `user1@test.com` / `password123`).
   - Create another account in Window B (e.g., `user2@test.com` / `password123`), **OR** just log in with the same account in both windows.

3. **Create a Project and Tasks:**
   - In Window A, create a new Project named "Alpha Launch".
   - Open the project board and create a couple of Tasks in the "To Do" column.

4. **Test the Live Update (SSE):**
   - Copy the URL of the project board from Window A (e.g., `http://localhost:3000/projects/<uuid>`).
   - Paste this URL into Window B so both windows are viewing the **exact same Kanban board side-by-side**.
   - Now, in Window A, **drag and drop a task** from "To Do" to "In Progress".
   - **Watch Window B:** You will see the task instantly move to "In Progress" simultaneously, without refreshing the page!

This live sync is powered by the FastAPI backend pushing an SSE `task_updated` event directly to the React frontend, which invalidates the React Query cache and automatically updates the local drag-and-drop state.

---

## ✨ Key Features

- **Real-Time Kanban Board:** Drag and drop tasks across columns (`To Do`, `In Progress`, `Done`). When a task is moved, the backend broadcasts the change using Server-Sent Events (SSE), instantly updating the UI for all connected users without a page refresh.
- **Project & Task Management:** Complete CRUD functionality for Projects and Tasks.
- **Secure Authentication:** JWT-based user authentication and secure endpoints.
- **SPA Routing Support:** The Dockerized Nginx frontend is explicitly configured to correctly handle React Router navigation, preventing 404 errors on page refreshes.

---

## 💻 Tech Stack

### Frontend
- **Framework:** React 19 + TypeScript
- **Build Tool:** Vite
- **State Management:** TanStack React Query (for server state) & Zustand (for client auth state)
- **Styling:** Tailwind CSS v4 & Shadcn UI
- **Routing:** React Router v7
- **Interactivity:** `@hello-pangea/dnd` for smooth drag-and-drop operations.
- **Real-time:** Native `EventSource` listening to backend SSE streams.

### Backend
- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL
- **ORM & Migrations:** SQLAlchemy (Async) & Alembic
- **Validation:** Pydantic
- **Real-time:** `asyncio.Queue` and `StreamingResponse` for Server-Sent Events (SSE).

---

## 🛠️ Development Setup

If you wish to run the project locally without Docker for development purposes:

### Database
Before running the backend, start the PostgreSQL database using Docker Compose:

```bash
cp .env.example .env  # If you haven't already
docker-compose up -d db
```

### Backend
We use `uv` for fast Python package management. Make sure you have it installed.

```bash
cd backend
uv sync

# Run database migrations (this will also seed initial test data)
# Seed user login: test@example.com / password123
uv run alembic upgrade head

# Start the development server
uv run uvicorn app.main:app --reload --port 8080
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
