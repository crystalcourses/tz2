# Django JSON Uploader

A simple Django web application for uploading JSON files, storing records in a database, and viewing them via a web interface.

## Tech Stack
- Python 3.10+
- Django 5.x
- SQLite (development)
- uWSGI
- Nginx

## Features
- Upload JSON files via web form
- Store uploaded records in the database
- View saved records in a table
- Ready-to-use configuration for deployment with uWSGI and Nginx

## Local Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
