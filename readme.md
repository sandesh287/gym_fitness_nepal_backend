
---

# ⚙️ **FastAPI Backend README**

```md
# 🧠 Fit Nepal - Backend API

FastAPI backend powering the Fit Nepal mobile application.

Handles:
- Authentication
- Gym management
- Class booking
- Membership plans
- Payments
- Admin features

---

## 🚀 Features

### 🔐 Authentication
- OTP-based login (mock)
- User profile management
- Role-based access (admin/user)

---

### 🏋️ Gym Management
- Create gym
- Update gym
- Delete gym
- Fetch gyms with filters:
  - Search
  - Location
  - Price range
  - Class availability

---

### 📅 Class Management
- Create classes per gym
- Assign trainers, time, duration
- Capacity & slot tracking
- Admin CRUD operations

---

### 📖 Booking System
- Book class
- Prevent duplicate bookings
- Cancel booking
- Booking history
- Auto slot adjustment

---

### 💳 Membership System
- Create membership after payment
- Track active membership
- Membership history
- Auto-expiry logic

---

### 🏷️ Membership Plans
- Dynamic plans per gym
- Admin CRUD operations
- Features list support
- Duration-based plans

---

### 💰 Payment Integration

#### Khalti
- Sandbox integration
- Payment initiation
- Payment verification

#### eSewa (Mock)
- Simulated payment API
- Backend-generated transaction
- Used for testing flow

---

## 🧱 Tech Stack

- FastAPI
- Python
- SQLAlchemy
- SQLite
- Pydantic
- HTTPX
- Uvicorn

---

## 📁 Project Structure

app/
├── main.py
├── api/
│ ├── routes/
│ ├── auth.py
│ ├── gym.py
│ ├── booking.py
│ ├── membership.py
│ ├── membership_plan.py
│ ├── payment.py
│ ├── user.py
│
├── models/
│ ├── user.py
│ ├── gym.py
│ ├── fitness_class.py
│ ├── booking.py
│ ├── membership.py
│ ├── membership_plan.py
│
├── schemas/
├── core/
│ ├── database.py



---

## ⚙️ Setup

### 1. Clone repo

```bash
git clone YOUR_BACKEND_REPO_URL
cd backend


### 2. Create virtual environment

```bash
python -m venv venv


### Activate:

### Windows:

```bash
venv\Scripts\activate


### Mac/Linux:

```bash
source venv/bin/activate


### 3. Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy httpx python-dotenv


### 4. Environment variables

#### Create .env:

```bash
KHALTI_SECRET_KEY=your_test_secret_key


### 5. Run server

```bash
uvicorn app.main:app --reload


### 🌐 API Base URL

```bash
http://127.0.0.1:8000/api/v1


### Docs:

```bash
http://127.0.0.1:8000/docs


## 📚 API Documentation

### 🔐 Auth

POST /auth/send-otp
POST /auth/verify-otp

### 👤 User
GET /users/profile
PUT /users/profile

### 🏋️ Gyms
GET /gyms/
POST /gyms/
PUT /gyms/{id}
DELETE /gyms/{id}


### Filters:

?search=
?location=
?min_price=
?max_price=
?class_title=


### 📅 Classes
GET /bookings/classes
POST /bookings/classes
PUT /bookings/classes/{id}
DELETE /bookings/classes/{id}


### 📖 Booking
POST /bookings/book
GET /bookings/history
PATCH /bookings/{id}/cancel


### 🏷️ Membership Plans
GET /membership-plans/
GET /membership-plans/gym/{gym_id}
POST /membership-plans/
PUT /membership-plans/{id}
DELETE /membership-plans/{id}


### 💳 Membership
POST /memberships/
GET /memberships/active
GET /memberships/history


### 💰 Payments
Khalti
POST /payments/khalti/initiate
POST /payments/khalti/lookup


### eSewa (Mock)
POST /payments/esewa/mock-pay


### 🗄️ Database

#### SQLite used for development
#### File:

gym_fitness.db

### Auto-created via:
Base.metadata.create_all(bind=engine)


## ⚠️ Notes
- Khalti is sandbox only
- eSewa is mock implementation
- Admin access is phone-based
- SQLite suitable for development only


## 📈 Future Improvements
- PostgreSQL migration
- JWT authentication
- Payment production integration
- Background jobs (expiry automation)
- Analytics dashboard
- Multi-admin roles