
# Ride sharing

RIde sharing is transportation based project

- **Customers** to participate in ride request.
- **Driver** to accept ride request and update the status.


## Project Setup

### 📌 Table of Contents
- [Clone the Repository](#clone-the-repository)
- [Create a Virtual Environment](#create-a-virtual-environment)
- [Setup Environment Variables](#setup-environment-variables)
- [Activate the Virtual Environment via Poetry](#activate-the-virtual-environment-via-poetry)
- [Install Dependencies](#install-dependencies)
- [Database setup](#database-setup)
- [Run Migrations](#run-migrations)
- [Create a Superuser](#create-a-superuser)
- [Run the Application](#run-the-application)


---

### Clone the Repository
Clone the repository to your local machine and navigate into the project directory:
```bash
git clone  https://github.com/shilpasasidharan97/ride_sharing.git
cd ride_sharing
```

### Create a Virtual Environment
Create and activate a virtual environment to isolate your dependencies,
Before that make sure your current shell is in the project python requirement ie, 3.13.1, Here we use pyenv to manage that:
```bash
$(pyenv which python) -m venv .venv -m venv .venv or virtualenv .venv -p $(pyenv which python)
source .venv/bin/activate  # On Windows: .venv\Scriptsctivate
```

### Setup Environment Variables

Before running the application, you need to create a .env file for environment variables. You can do this by copying the example file:

```bash
cp .env.example .env
touch .env.override
```

### Activate the Virtual Environment via Poetry
You can activate the virtual environment:
```bash
source .venv/bin/activate  # On Windows: .venv\Scriptsctivate
```

Once copied, open .env and update the necessary variables according to your local setup. Use .env.override to temporary overraid .env

### Install Dependencies
Install all required dependencies using Poetry:
```bash
pip install -r requirements.txt
```


### Database setup
Ensure PostgreSQL is installed and running. Then create the database and user:
```bash
sudo -u postgres psql
CREATE DATABASE <DB NAME>;
CREATE USER <USER> WITH PASSWORD <password>;
GRANT ALL PRIVILEGES ON DATABASE <DB NAME> TO <USER>;
\c <DB NAME>
CREATE EXTENSION postgis;
```


### Run Migrations
```bash
python manage.py migrate
```

## Create a Superuser
creating a superuser is optional
```bash
python manage.py createsuperuser
```

### Run the Application
```bash
python manage.py runserver
```

---

