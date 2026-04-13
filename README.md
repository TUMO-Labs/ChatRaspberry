# ChatRaspberry

A simple web-based chat application built with **Flask** and **SQLite**.  
It supports user registration, login, and real-time message posting with a persistent chat history.

## Tech Stack

- **Python 3**
- **Flask 3.1** — web framework
- **Flask-SQLAlchemy 3.1** — database ORM
- **SQLite** — lightweight file-based database
- **Werkzeug** — password hashing (built into Flask)

## Project Structure

```
ChatRaspberry/
├── chat/
│   ├── app.py               # Flask app, routes, and database models
│   ├── requirements.txt     # Python dependencies
│   ├── run.sh               # Setup and launch script
│   └── templates/
│       ├── register.html    # Registration page
│       ├── login.html       # Login page
│       └── index.html       # Chat page (message history + send/delete)
├── nginx/
│   └── chat.conf            # nginx server config (proxies port 80 → Flask)
├── run.sh                   # Root launch script
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
- Install **Python 3** if not found (via `apt`)
- Install **nginx** if not found (via `apt`)
- Copy `nginx/chat.conf` to `/etc/nginx/sites-available/` and symlink to `sites-enabled/`
- Restart nginx
- Create a Python virtual environment
- Install dependencies from `chat/requirements.txt`
- Start the Flask server

### 3. Open in browser

```
http://<raspberry-pi-ip>
```

nginx listens on port **80** and forwards requests to Flask on port **5000**, so no port number is needed.

> For local development, access Flask directly at `http://127.0.0.1:5000`

## How It Works

1. Visit `/register` → create an account (username + password, stored hashed)
2. Visit `/login` → log in with your credentials
3. Visit `/` → see all past messages (newest first)
4. Type a message → click **Send** → saved to DB under your username
5. Click **Delete** on your own messages → removed from DB
6. Click **Logout** → session cleared, redirected to login

> Only your own messages show the Delete button.

## Routes

| Route | Method | Description |
|---|---|---|
| `/register` | GET, POST | Register a new user |
| `/login` | GET, POST | Log in |
| `/` | GET, POST | Chat page (send & delete messages) |
| `/logout` | GET | Clear session and redirect to login |

## Database

The app uses two tables stored at `chat/instance/chat.db`:

**`user`**

| Column   | Type        | Description                  |
|----------|-------------|------------------------------|
| id       | Integer     | Auto-incremented primary key |
| username | String(50)  | Unique username              |
| password | String(200) | Hashed password              |

**`message`**

| Column    | Type        | Description                   |
|-----------|-------------|-------------------------------|
| id        | Integer     | Auto-incremented primary key  |
| username  | String(50)  | Sender's username             |
| content   | String(500) | Message text                  |
| timestamp | DateTime    | Time the message was sent     |

## Features

- User Registration — Create an account with username & password
- Login/Logout — Secure authentication with hashed passwords
- Chat Room — Send and view messages in a shared space
- Message History — Persistent storage in SQLite
- Timestamps — Each message includes the time it was sent
- Responsive UI — Styled with modern CSS for a clean look

## Database

The app uses a `message` table:

| Column    | Type         | Description              |
|-----------|--------------|--------------------------|
| id        | Integer      | Auto-incremented primary key |
| username  | String(50)   | Sender's name            |
| content   | String(500)  | Message text             |
| timestamp | DateTime     | Time the message was sent |

The app also uses a  `user` table:

| Column    | Type         | Description              |
|-----------|--------------|--------------------------|
| id        | Integer      | Auto-incremented primary key |
| username  | String(50)   | Unique username          |
| password  | String(200)  | Hashed password             |


## Security

- Passwords are stored securely using Werkzeug’s hashing functions.

