# ChatRaspberry

A simple web-based chat application built with Flask and SQLite. Users can send messages with a username and view the full chat history on a single page.

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
│       └── index.html       # Chat page (form + message history)
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

## How It Works

- Visit the page → see all past messages
- Enter a username and message → click **Send**
- The message is saved to `instance/chat.db` (SQLite) and shown on the page

## Database

The app uses a single `message` table:

| Column    | Type         | Description              |
|-----------|--------------|--------------------------|
| id        | Integer      | Auto-incremented primary key |
| username  | String(50)   | Sender's name            |
| content   | String(500)  | Message text             |
| timestamp | DateTime     | Time the message was sent |