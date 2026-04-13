# ChatRaspberry

A simple web-based chat application built with **Flask** and **SQLite**.  
It supports user registration, login, and real-time message posting with a persistent chat history.

## Tech Stack

- **Python 3**
- **Flask 3.1** — web framework
- **Flask-SQLAlchemy 3.1** — database ORM
- **SQLite** — lightweight file-based database

## Project Structure

```
ChatRaspberry/
├── chat/
│   ├── app.py               # Flask app, routes, and database models
│   ├── requirements.txt     # Python dependencies
│   ├── run.sh               # Setup and launch script
│   └── templates/
│       ├── index.html       # Chat page (messages + form)
│       ├── login.html       # Login page
│       └── register.html    # Registration page
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/TUMO-Labs/ChatRaspberry.git
```

### 2. Run the app

```bash
chmod +x ./run.sh
./run.sh
```

The script will:
- Check if Python 3 is installed
- Create a virtual environment
- Install dependencies from `requirements.txt`
- Start the Flask development server

### 3. Open in browser

```
http://127.0.0.1:5000
```

## Features

- User Registration — Create an account with username & password
- Login/Logout — Secure authentication with hashed passwords
- Chat Room — Send and view messages in a shared space
- Message History — Persistent storage in SQLite
- Timestamps — Each message includes the time it was sent
- Responsive UI — Styled with modern CSS for a clean look

## Database

The app uses a single `message` table:

| Column    | Type         | Description              |
|-----------|--------------|--------------------------|
| id        | Integer      | Auto-incremented primary key |
| username  | String(50)   | Sender's name            |
| content   | String(500)  | Message text             |
| timestamp | DateTime     | Time the message was sent |
