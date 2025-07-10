# 🏥 Hospital Management System (HMS)

A modern web-based Hospital Management System built with **Django**, powered by **PostgreSQL**, and integrated with **Stripe** for secure hospital billing.

![Main](screenshots/System_Features.png)

---

## 🚀 Features

- 🧑‍⚕️ Role-based access (Admin, Doctor, Patient)
- 📅 Appointment booking & doctor availability
- 📁 Patient medical records & history
- 💳 Stripe payment integration
- 📊 Admin dashboard with analytics
- 🔐 Secure login & user management

---

## ⚙️ Tech Stack

- **Backend**: Django
- **Database**: PostgreSQL
- **Payments**: Stripe
- **Frontend**: Bootstrap + Django templates
- **Deployment**: Compatible with Heroku, Render, etc.

---

## 📸 Dashboards

| 🧑 Patient Dashboard | 🥼 Doctor Dashboard | 🧑‍💼 Admin Dashboard |
|----------------------|---------------------|----------------------|
| ![Patient](screenshots/Doctor_Profile.png) | ![Doctor](screenshots/Patient_Profile.png) | ![Admin](screenshots/Admin_Dash.png) |

---

## 📦 Installation

```bash
# Clone the project
git clone https://github.com/yourusername/hms.git
cd hms

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up PostgreSQL in settings.py or .env
# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run server
python manage.py runserver
