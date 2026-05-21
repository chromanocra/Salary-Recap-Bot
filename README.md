# Telegram Salary Recap Bot

A simple Python-based Telegram bot to automatically scrape billing messages in a group, calculate the commission split between the agency and the talent, and generate a neatly formatted recap automatically.

## Features
- **Automatic Salary Recap:** Instantly parses bill data and formats it perfectly.
- **FastAPI Integrated:** Ready for modern web framework scaling.
- **Built-in Dummy Server:** Integrated with a lightweight server to keep it running smoothly on web service hosting.

## Project Folder Structure

```text
salaryRecap_bot/
├── app/
│   └── main.py         # Main bot & Dummy Server for Render deployment
├── config/
│   └── service.py      # Text processing logic (Regex) & salary calculation
├── .env                # Secure bot token storage (optional)
└── requirements.txt    # List of required Python libraries