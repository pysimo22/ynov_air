# Ynov Air Project

This project is a **Django web application** for managing flights, passengers, bookings, and baggage. It uses **SQLite / SQL database** for storing all flight and booking information.

---

## Features

- View flights and flight details
- Manage passengers and bookings
- Track baggage per passenger
- Analyze data with SQL queries:
  - Total revenue per month
  - Most popular airports
  - Occupancy rates per flight
  - Top 10 most profitable routes

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/pysimo22/ynov_air.git
cd ynov_air
```

2. **Create a virtual environment**

```bash
python -m venv venv
```

3. **Activate the virtual environment**

- On Windows:

```bash
venv\Scripts\activate
```

- On Mac/Linux:

```bash
source venv/bin/activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Setup Database

1. Make sure your database (SQLite) is ready.
2. Apply Django migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

3. (Optional) Create a superuser to access the admin:

```bash
python manage.py createsuperuser
```

---

## Running the Django Project

Start the development server:

```bash
python manage.py runserver
```

Open your browser and go to:

```
http://127.0.0.1:8000/
```

To access the Django admin:

```
http://127.0.0.1:8000/admin/
```

---

## Using the Database

- You can execute SQL queries directly in the **SQLite database** using **DB Browser for SQLite** or Django ORM.
- All SQL queries for analytics, reports, and baggage management are included in the project.

---

## Project Structure

```
ynov_air/
├─ flights/         # Django app for flights and bookings
├─ manage.py        # Django management script
├─ db.sqlite3       # SQLite database
├─ README.md
└─ requirements.txt
```

---

## Notes

- Use Django ORM for CRUD operations on flights, passengers, bookings, and baggage.
- SQL queries can be executed in DB Browser or Django `connection.cursor()` for advanced analytics.
- Make sure the virtual environment is activated before running any Django commands.
