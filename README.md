# Real-Time Chat Hub with FastAPI & WebSockets

A full-stack real-time chat application built with FastAPI, WebSockets, Vue.js, and SQLite/PostgreSQL.

---

## 🚀 Features

- **Real-time messaging** via WebSockets
- **User authentication** using JWT tokens
- **Multiple chat rooms** (public & private)
- **Message persistence** in SQL database
- **Modern Vue.js frontend** (responsive, SPA)
- **RESTful API** for user/room management

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** — Python web framework
- **WebSockets** — Real-time communication
- **SQLModel** — ORM (Pydantic + SQLAlchemy)
- **SQLite/PostgreSQL** — Persistent storage
- **JWT** — Token-based authentication

### Frontend
- **Vue.js 3** — Progressive JS framework
- **Pinia** — State management
- **Vue Router** — Routing
- **Axios** — HTTP client
- **Vite** — Fast dev/build tool

---

## ⚡ Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+

---

### 1. Clone the Repository

```bash
git clone https://github.com/Kirankumarvel/fastapi-websocket-chat-hub.git
cd fastapi-websocket-chat-hub
```

---

### 2. Backend Setup

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI backend server
uvicorn backend.main:app --reload
```

---

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

### 4. Open in Browser

- **Frontend:** [http://localhost:3000](http://localhost:3000)
- **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 💬 Usage

1. **Register** a new user account
2. **Login** with your credentials
3. **Create** a chat room or **join** an existing one
4. **Chat in real-time** with other users

---

## 🔗 API Endpoints

| Method | Endpoint                | Description                        |
|--------|-------------------------|------------------------------------|
| POST   | `/token`                | User login                         |
| POST   | `/register`             | User registration                  |
| GET    | `/rooms`                | List all chat rooms                |
| POST   | `/rooms`                | Create a new chat room             |
| GET    | `/rooms/{room_id}/messages` | Get messages for a room        |
| WS     | `/ws/{room_id}`         | WebSocket endpoint for chat        |

---

## 📁 Project Structure

```
fastapi-websocket-chat-hub/
├── backend/           # FastAPI backend application
├── frontend/          # Vue.js frontend application
├── tests/             # Test files
├── docker-compose.yml # Docker configuration for full stack
├── Dockerfile         # Backend Dockerfile
├── requirements.txt   # Python dependencies
├── .env.example       # Sample environment config
└── README.md          # This file
```

---

## 🚢 Deployment

### Docker Deployment

```bash
docker-compose up -d
```

### Manual Deployment

- **Set environment variables** (see `.env.example`)
- For production, use PostgreSQL:
  ```python
  # backend/config.py
  DATABASE_URL = "postgresql://user:password@localhost:5432/chatdb"
  ```

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create a branch:** `git checkout -b feature-name`
3. **Commit:** `git commit -am 'Add feature'`
4. **Push:** `git push origin feature-name`
5. **Submit a Pull Request**

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [FastAPI documentation](https://fastapi.tiangolo.com/) and community
- [Vue.js documentation](https://vuejs.org/) and examples
- [SQLModel](https://sqlmodel.tiangolo.com/) for excellent DB integration

---

