# ChatRaspberry

A web-based chat application built with **Flask** and **SQLite**, featuring real-time messaging via WebSockets, user authentication, and message encryption.

## Tech Stack

- **Python 3**
- **Flask 3.1** — web framework
- **Flask-SQLAlchemy 3.1** — database ORM
- **Flask-SocketIO** — WebSocket support for real-time messaging
- **SQLite** — lightweight file-based database
- **Werkzeug** — password hashing
- **cryptography (Fernet)** — symmetric encryption for stored messages
- **Gunicorn** — production WSGI server (gthread worker)
- **nginx** — reverse proxy

## Project Structure

```
ChatRaspberry/
├── chat/
│   ├── app.py               # Flask app, routes, models, WebSocket events
│   ├── requirements.txt     # Python dependencies
│   ├── secret.key           # Fernet encryption key (auto-generated, do not commit)
│   └── templates/
│       ├── register.html    # Registration page
│       ├── login.html       # Login page
│       └── index.html       # Chat page (real-time messaging + delete)
├── nginx/
│   └── chat.conf            # nginx config (proxy + WebSocket headers)
├── chat.service             # systemd service file for Raspberry Pi
├── run.sh                   # Setup and launch script (macOS + Raspberry Pi)
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/TUMO-Labs/ChatRaspberry.git
cd ChatRaspberry
```

### 2. Run the setup script

```bash
chmod +x ./run.sh
./run.sh
```

The script will:
- Install **Python 3** if not found
- Install **nginx** if not found (Raspberry Pi only)
- Copy `nginx/chat.conf` to nginx config directory
- Create a Python virtual environment and install dependencies
- **On Raspberry Pi:** install and start a systemd service so the app runs in the background and auto-starts on boot
- **On macOS:** start Gunicorn directly in the terminal

### 3. Open in browser

```
http://<raspberry-pi-ip>        # via nginx on port 80
http://localhost:8080            # macOS dev (nginx on port 8080)
```

## Features

- **Real-time messaging** — WebSocket (Flask-SocketIO) pushes new messages to all connected users instantly, no page refresh needed
- **User authentication** — Register/login/logout with hashed passwords
- **Message encryption** — All messages are encrypted with Fernet before being stored in the DB
- **Delete own messages** — Only the sender sees a delete button on their messages
- **Persistent history** — Messages survive restarts, loaded from DB on page open
- **Timestamps** — Each message shows the time it was sent

## Routes

| Route | Method | Description |
|---|---|---|
| `/register` | GET, POST | Register a new user |
| `/login` | GET, POST | Log in |
| `/` | GET | Chat page (loads history, opens WebSocket) |
| `/logout` | GET | Clear session and redirect to login |

## WebSocket Events

| Event | Direction | Description |
|---|---|---|
| `send_message` | Client → Server | Send a new message |
| `new_message` | Server → All clients | Broadcast a new message to everyone |

## Database

**`message` table:**

| Column    | Type         | Description                   |
|-----------|--------------|-------------------------------|
| id        | Integer      | Auto-incremented primary key  |
| username  | String(50)   | Sender's name                 |
| content   | String(1000) | Fernet-encrypted message text |
| timestamp | DateTime     | Time the message was sent     |

**`user` table:**

| Column   | Type        | Description                  |
|----------|-------------|------------------------------|
| id       | Integer     | Auto-incremented primary key |
| username | String(50)  | Unique username              |
| password | String(200) | Werkzeug-hashed password     |

## Security

- Passwords hashed with Werkzeug (`pbkdf2:sha256`)
- Messages encrypted at rest with Fernet symmetric encryption
- Encryption key stored in `chat/secret.key` (auto-generated on first run, never committed to git)
- Session cookies signed with Flask `SECRET_KEY`
