country_exchange_api
A Django REST API that provides country information, exchange rates, and computed GDP estimates.
It integrates live data from external APIs, supports CRUD operations, and generates visual summary reports as images.

This project is built for easy local development using SQLite and deploys seamlessly to PythonAnywhere.


---

🚀 Features

GET /countries — Fetch all countries (supports filtering and sorting).

GET /countries/:name — Retrieve a specific country.

DELETE /countries/:name — Delete a country record.

POST /countries/refresh — Refresh data from external APIs and compute GDP.

GET /countries/status — Get database status and last refresh timestamp.

GET /countries/image — Return a generated summary report image.



---

🧱 Project Structure

country_exchange_api/
│
├── currency/                 # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── countries/              # Main API app
│   ├── models.py
│   ├── views.py
│   ├── utils.py
│   ├── image_utils.py
│   ├── urls.py
│   └── migrations/
│
├── manage.py
├── requirements.txt
├── .env.example
└── README.md


---

⚙ Setup Instructions (Run Locally)

🧩 Prerequisites

Ensure you have installed:

Python 3.10+

Git


🧩 1. Clone the Repository

git clone https://github.com/Sjaypeter/Country_exchange_api.git


🧩 2. Create and Activate Virtual Environment

python -m venv venv
source venv/bin/activate    # For macOS/Linux
venv\Scripts\activate       # For Windows

🧩 3. Install Dependencies

pip install -r requirements.txt

🧩 4. Create Environment Variables File

Create a .env file in the project root and copy the content below 👇

DJANGO_SECRET_KEY=replace_me
DEBUG=True
USE_SQLITE=True
TIME_ZONE=Africa/Lagos
PORT=8000

(SQLite is used by default for local development — no extra DB setup required.)

🧩 5. Apply Migrations

python manage.py migrate

🧩 6. Run the Development Server

python manage.py runserver

Then visit: 👉 http://127.0.0.1:8000/countries


---

📦 List of Dependencies

Package	Description

Django>=4.2	Web framework
djangorestframework	For REST API views and serialization
requests	To fetch external country/exchange data
python-dotenv	For environment variable management
Pillow	For generating image reports
pytz	For timezone handling
mysqlclient (optional)	For production database (if not using SQLite)
whitenoise	For static file serving in production
gunicorn	For WSGI server on deployment



---

🔑 Environment Variables

Variable	Description	Example

DJANGO_SECRET_KEY	Django secret key	replace_me
DEBUG	Enable debug mode (True for local only)	True
USE_SQLITE	Use SQLite (True) or MySQL (False)	True
TIME_ZONE	Timezone for your app	Africa/Lagos
DB_NAME	(Optional) MySQL database name	exchange_db
DB_USER	(Optional) MySQL username	root
DB_PASSWORD	(Optional) MySQL password	password
DB_HOST	(Optional) MySQL host	127.0.0.1
DB_PORT	(Optional) MySQL port	3306
PYTHONANYWHERE_HOST	(For deployment) Domain of hosted app	mangi.pythonanywhere.com



---

🧠 How to Test the API

Example: Refresh All Countries

curl -X POST http://127.0.0.1:8000/countries/refresh

Example: Get All Countries

curl http://127.0.0.1:8000/countries

Example: Get Countries by Region

curl "http://127.0.0.1:8000/countries?region=Africa"

Example: Fetch Country Details

curl http://127.0.0.1:8000/countries/Nigeria

Example: Generate and Download Image Summary

curl http://127.0.0.1:8000/countries/image --output summary.png


---

🌐 Deployment Guide (PythonAnywhere)

1. Push code to GitHub


2. Clone it on PythonAnywhere:

git clone https://github.com/Sjaypeter/Country_exchange_api.git
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt





4. Edit WSGI file with environment vars.


5. Run:

python manage.py migrate
python manage.py collectstatic


6. Reload the app.




---

🧾 License

This project is open-source under the MIT License.
Feel free to use, modify, and contribute.


---

✅ Author: Udeagha Mark Mang
Backend Developer | Empathy-driven Software Engineer | Passionate about solving real-world problems through code.
