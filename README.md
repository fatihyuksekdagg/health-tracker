# 🏥 Health Tracker - Flask Web App

**Health Tracker** is a web-based personal health monitoring application built with Flask.

It allows users to:
- Log daily steps, water intake, and sleep hours
- Set personal goals and track progress
- View weekly charts (steps, water, sleep)
- Register, log in, and update profile details
- Toggle between light and dark theme modes

## ✨ Features
- 👤 User Authentication (Login / Signup)
- 🎯 Daily Goal Tracking with Progress Bars
- 📈 Weekly Statistics with Line Charts
- 🌙 Theme Toggle (Light / Dark Mode)
- 🗃️ SQLite3 Database Integration
- 📱 Mobile-friendly Design with Bootstrap 5

## 🚀 Tech Stack
- Python
- Flask
- SQLite
- Bootstrap 5
- HTML + Jinja2 Templates

## 📁 Folder Structure
```
health_tracker/
├── app.py
├── database.db
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── history.html
│   ├── stats.html
│   ├── profile.html
│   └── change_password.html
├── static/
│   └── (optional CSS / images)
├── update_users_table.py
└── README.md
```

## 📌 Setup Instructions
1. Clone the repository
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the database updater:
    ```bash
    python update_users_table.py
    ```
4. Start the app:
    ```bash
    python app.py
    ```
5. Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser

## 💡 Future Plans
- Google Fit or Apple Health integration
- Export to CSV and weekly email reports
- Mobile app version (Flutter or React Native)
