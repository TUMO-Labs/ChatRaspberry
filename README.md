# ChatRaspberry

A simple web-based chat application built with Flask and SQLite, served through nginx. Users can send and delete messages with a username and view the full chat history on a single page.

## Tech Stack

- **Python 3**
- **Flask 3.1** — web framework
- **Flask-SQLAlchemy 3.1** — database ORM
- **SQLite** — lightweight file-based database
- **nginx** — reverse proxy (forwards port 80 → Flask on port 5001)

## Project Structure

```
ChatRaspberry/
├── chat/
│   ├── app.py               # Flask app, routes, and database models
│   ├── requirements.txt     # Python dependencies
│   ├── run.sh               # Setup and launch script
│   └── templates/
│       └── index.html       # Chat page (form + message history)
├── nginx/
│   └── chat                 # nginx server config
├── run.sh                   # Root launch script
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/TUMO-Labs/ChatRaspberry.git
cd ChatRaspberry
```

### 2. Install nginx (if not already installed)

```bash
brew install nginx
```

### 3. Set up nginx config

```bash
sudo cp nginx/chat /etc/nginx/servers/chat
sudo nginx -s reload
```

### 4. Run the Flask app

```bash
chmod +x ./run.sh
./run.sh
```

The script will:
- Check if Python 3 is installed
- Create a virtual environment inside `chat/`
- Install dependencies from `requirements.txt`
- Start the Flask server on port **5001**

### 5. Open in browser

```
http://127.0.0.1:5001
```

nginx listens on port 80 and forwards requests to Flask on port 5001, so no port number is needed.

> For development without nginx, access Flask directly at `http://127.0.0.1:5001`

## How It Works

- Visit the page → see all past messages (newest first)
- Enter a username and message → click **Send** → saved to DB
- Click **Delete** next to any message → removed from DB
- After every action the page redirects (POST → Redirect → GET) to prevent duplicate submissions on refresh

## Database

The app uses a single `message` table stored at `chat/instance/chat.db`:

| Column    | Type         | Description                   |
|-----------|--------------|-------------------------------|
| id        | Integer      | Auto-incremented primary key  |
| username  | String(50)   | Sender's name                 |
| content   | String(500)  | Message text                  |
| timestamp | DateTime     | Time the message was sent     |