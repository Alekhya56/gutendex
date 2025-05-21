 📚 Books API - Django REST Framework

A RESTful API built using **Django** and **Django REST Framework** to serve book data with support for advanced filtering, full-text search, pagination.

---

## 🚀 Features

- Retrieve books with filter criteria:
  - Filter by language, topic, mime type, author, title
  - Support for multiple values per filter: `?language=en,fr`
- Full-text search on title, authors, and subjects
- Sort books by download count (popularity)
- Pagination (25 results per page)
- Modular, clean project structure
- Production-ready codebase

---

## 📦 Tech Stack

- Python 3.13.3
- Django
- Django REST Framework
- PostgreSQL


---

## 📄 API Documentation

Application is available at: http://127.0.0.1:8000/api/books/

# 🔍 Filter & Search Examples

- Filter by language and topic: /api/books/?language=en,fr&topic=child,infant

- Filter by title:/api/books/?title=history

- Filter by author: /api/books/?author=Jefferson

- With Pagination: /api/books/?author=Jefferson&page=2

🔧 Setup Locally

Open bash:

git clone https://github.com/Alekhya56/gutendex.git
cd books-api

# Create virtualenv
python -m venv env
source env/bin/activate

# Install requirements
pip install -r requirements.txt

# Run migrations (if using managed=True)
python manage.py migrate

# Run server
python manage.py runserver

👨‍💻 Author
Developed by Alekhya Ravada

