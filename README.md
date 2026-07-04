# GRMS — Graduate Research Management System

A web-based platform built for the  Federal Urdu University of Arts, Science & Technology (FUUAST)  to digitize and centralize the entire graduate research lifecycle — from student admission to synopsis review, thesis evaluation, and final degree issuance.

**Live App:** https://grms-production.up.railway.app/

---

## ✨ Features

- Role-based dashboards for **Admin, Student, Supervisor, and Examiner**
- Synopsis submission & multi-stage approval workflow
- Thesis evaluation with examiner assignment and viva result tracking
- Meeting record scheduling and history
- Extension case tracking and approvals
- Automated PDF degree letter generation
- Secure, session-based authentication with role-based access control

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.2.7 (Python) |
| Frontend | HTML5, CSS3, JavaScript, Bootstrap 5 |
| Database | MySQL (normalized, 3NF) |
| Static Files | WhiteNoise |
| App Server | Gunicorn |
| Containerization | Docker |
| Hosting | Railway |

Full dependency list is in [`requirements.txt`](requirements.txt).

---

## 💻 Running Locally with WAMP

This guide sets up GRMS on **Windows using WAMP Server** (Apache + MySQL), which is what the project was originally developed on.

### 1. Prerequisites

Install the following before starting:

- **[WAMP Server](https://www.wampserver.com/)** (provides MySQL + phpMyAdmin)
- **[Python 3.12](https://www.python.org/downloads/)** (make sure "Add Python to PATH" is checked during install)
- **[Git](https://git-scm.com/downloads)**

### 2. Start WAMP and create the database

1. Launch **WAMP Server** — wait until the tray icon turns **green** (all services running).
2. Open **phpMyAdmin** by clicking the WAMP icon → `phpMyAdmin`, or visit `http://localhost/phpmyadmin/`.
3. Click **New** on the left sidebar and create a database, e.g.:
   ```
   grms_db
   ```
4. Leave the default WAMP MySQL credentials as they are (usually user `root` with no password), or note down your custom credentials — you'll need them in step 5.

### 3. Clone the repository

```bash
git clone https://github.com/alishba158/GRMS.git
cd GRMS
```

### 4. Create a virtual environment & install dependencies

```bash
python -m venv venv
venv\Scripts\activate        # On Windows
pip install -r requirements.txt
```

> **Note:** `mysqlclient` sometimes fails to install on Windows if MySQL's dev headers aren't found. If it fails, install the matching prebuilt wheel from [https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient), or install via `pip install mysqlclient --only-binary :all:`.

### 5. Configure the database connection

Open `grms_project/settings.py` and update the `DATABASES` section to match your WAMP MySQL setup:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'grms_db',
        'USER': 'root',
        'PASSWORD': '',          # your WAMP MySQL password, if you set one
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 6. Run migrations & create an admin account

```bash
python manage.py migrate
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password for the Admin role.

### 7. Collect static files (optional for local dev, required before deploying)

```bash
python manage.py collectstatic
```

### 8. Run the development server

```bash
python manage.py runserver
```

Open your browser at:

```
http://127.0.0.1:8000/
```

Log in to the admin dashboard at `http://127.0.0.1:8000/admin/` with the superuser account created in step 6.

---

## 🚀 How It Runs After Deployment (Railway)

In production, GRMS runs differently from the local WAMP setup — it's containerized and served by Gunicorn instead of Django's development server.

### Deployment flow

1. **Dockerfile builds the image** — installs system dependencies (`default-libmysqlclient-dev`, `gcc`), then installs Python packages from `requirements.txt`.
2. **Static files are collected at build time** — `python manage.py collectstatic --no-input` runs inside the Docker build step, and **WhiteNoise** serves these static files directly in production (no separate web server like Nginx needed).
3. **Gunicorn serves the app** — instead of `runserver`, production uses:
   ```bash
   gunicorn grms_project.wsgi:application --bind 0.0.0.0:8000
   ```
   Gunicorn is a production-grade WSGI server that handles multiple concurrent requests reliably, unlike Django's built-in dev server.
4. **The database is hosted separately on filess.io** — instead of a local WAMP MySQL instance, production uses a **remote MySQL database provisioned on [filess.io](https://filess.io)**. Railway doesn't host the database itself; it simply connects to filess.io over the network using credentials stored as environment variables (see below).
5. **The app is exposed publicly** at the Railway-generated domain (or a custom domain if configured).

### Setting up the database on filess.io

1. Sign up / log in at **[filess.io](https://filess.io)**.
2. Create a new **MySQL** database instance from the dashboard.
3. Once created, filess.io gives you a connection panel with:
   - **Hostname**
   - **Port**
   - **Database name**
   - **Username**
   - **Password**
4. Copy these values — you'll paste them into Railway's environment variables next (don't hardcode them in `settings.py`).
5. Optional: use filess.io's built-in web-based DB client (or connect via MySQL Workbench / phpMyAdmin using the given host/port) to inspect tables after migrations are run.

### Connecting filess.io to Railway

1. Open your project on **[Railway](https://railway.app)** → select the GRMS service → go to the **Variables** tab.
2. Add the filess.io credentials as environment variables, e.g.:
   ```
   DB_NAME=your_filess_db_name
   DB_USER=your_filess_username
   DB_PASSWORD=your_filess_password
   DB_HOST=your_filess_hostname
   DB_PORT=your_filess_port
   ```
3. Make sure `grms_project/settings.py` reads these instead of hardcoded local values (see the `os.environ.get(...)` pattern below).
4. Redeploy the Railway service (or let it auto-redeploy on the next `git push`) so the new variables take effect.
5. Once live, run migrations against the remote database from Railway's shell/console (Railway dashboard → your service → **Shell**):
   ```bash
   python manage.py migrate
   ```
6. Verify the connection by opening the live app and confirming login/data loads correctly — if it fails, double-check the filess.io host/port allow external connections and that the credentials match exactly (no trailing spaces).

### Environment variables (production)

Rather than the hardcoded local values in step 5 above, production reads database credentials and secrets from environment variables — pointing to the **filess.io** database instead of local WAMP MySQL. A typical pattern:

```python
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
```

These variables are set in **Railway's project dashboard → Variables tab**, not committed to the repo.

### Redeploying after changes

Railway rebuilds and redeploys automatically whenever changes are pushed to the connected GitHub branch (CI/CD via GitHub webhook) — there's no need to manually restart the server after `git push`.

---

## 📁 Project Structure

```
GRMS/
├── accounts/           # User auth, roles, and profile logic
├── grms_project/       # Django project settings, URLs, WSGI entry point
├── media/              # User-uploaded files (synopsis, thesis PDFs, etc.)
├── static/              # CSS, JS, images
├── templates/           # HTML templates
├── Dockerfile           # Container build definition for deployment
├── manage.py            # Django management CLI
├── requirements.txt      # Python dependencies
└── runtime.txt           # Python runtime version pin
```

---

## 👥 Developed By

- **Alishba Arshad** — Group Leader
- **Sana Tariq** — Group Member

**Supervised by:** Dr. Kashif Rizwan
**Department of Computer Science, FUUAST, Islamabad**
**Session: BSCS [2022 – 2026]**

---

## 📄 License

This project was developed as a final-year academic requirement for the award of a BS Computer Science degree at FUUAST. All rights reserved by the authors.
