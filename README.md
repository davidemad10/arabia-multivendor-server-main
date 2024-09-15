# Project Name

 Arabia-multivendor-server


## Table of Contents
- [Project Setup](#project-setup)
- [Running the Project](#running-the-project)
- [Environment Variables](#environment-variables)
- [Database Migration](#database-migration)
- [Create a Superuser](#create-a-superuser)

---

## Project Setup

### 1. Clone the Repository
First, clone the repository to your local machine:
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
### 2. Create a Virtual Environment
Set up a Python virtual environment to isolate project dependencies:
```bash
python -m venv venv
```
### 3. Activate the Virtual Environment
After creating the virtual environment, activate it:
```bash
venv\Scripts\activate
```
### 4. Install Dependencies
Make sure you have pip installed and install the necessary dependencies:
```bash
pip install -r requirements.txt
```
### 5. Environment Variables
The project uses environment variables for sensitive settings like database credentials, secret keys, etc.

##### Option 1: If you have access to the .env file, place it in the root of the project.
##### Option 2: If no .env file is provided, create one by referring to .env.example or ask the project maintainer for details.

Example .env file setup:
```bash
DB_NAME=Data Base Name
DB_USER= User Name Of Postgres
DB_PASSWORD= Data Base Password
DB_HOST= Data Base Host
DB_PORT= Data Base Port
```

# Running the Project
### 6.Apply Migrations
Before running the server, you need to apply the database migrations:
```bash
python manage.py migrate
```
### 7.Run the Development Server
```bash
python manage.py runserver
```
Now, the server will be available at http://127.0.0.1:8000/.
