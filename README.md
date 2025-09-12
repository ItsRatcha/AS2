# Room Booking Django Web App
This is a roombooking web app that allows students to book rooms. This project is a part of an assignment for class CN331.

![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)
![Build Status](https://img.shields.io/badge/progress-100-brightgreen)

---
![title](Screenshots/Title.jpg)

## Features

### Student features
- Look up rooms
- Look up available time for each room
- Look up your booked room
- Cancel your booking
- Easily book rooms with real-time availability

### Staff features
- Book multiple rooms without restriction
- Can create, edit or remove users
- Can create, edit or remove anyone's booking
- Can create, edit or remove rooms

## Technology Stack
- Backend: Python, Django
- Frontend: Django Templates, Tailwind CSS, JavaScript
- Database: SQLite3 (for development)
- Development Tools: Git, Virtualenv

## Prerequisites
Before you begin, ensure you have the following installed on your system:
- Python (3.8 or newer)
- pip (Python package installer)
- Git
- Node.js

## How to run
1. Clone the repository:
   ```
   git clone https://github.com/ItsRatcha/AS2.git
   ```
2. (Optional but recommended) Create and activate a virtual environment:
   ```
   # For Windows
   python -m venv .venv
   .\.venv\Scripts\activate

   # For macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Apply database migrations: This will set up the necessary database tables.
   ```
   python manage.py migrate
   ```
5. Create a superuser: This account will have staff/admin privileges. Follow the prompts to create a username and password.
   ```
   python manage.py createsuperuser
   ```
6. Run the development server: This command starts both the Django server and the Tailwind CSS compiler.
   ```
   python manage.py tailwind dev
   ```
   *Alternatively, you can run them in separate terminal windows:*
   ```
   # In terminal 1:
   python manage.py runserver

   # In terminal 2:
   python manage.py tailwind start
   ```
7. Open your web browser and navigate to [http://127.0.0.1:8000/.](http://127.0.0.1:8000/.)

Contributions are welcome! Feel free to open issues or submit PRs.

## Screenshots

*Main landing page for all users.*
![screenshot1](Screenshots/Screenshot1.png)
*Dashboard showing current bookings.*
![screenshot2](Screenshots/Screenshot2.png)
*Rooms overview with real-time availability display*
![screenshot3](Screenshots/Screenshot3.png)
*Room detail and availability*
![screenshot4](Screenshots/Screenshot4.png)

## Video guide

The video guide and introduction is up on Youtube: [youtu.be/hjAHmUp8uWc](https://youtu.be/hjAHmUp8uWc) (Note that the spoken language is Thai as per professor's preference)

## Author
Ratchanon Moungwichean, undergraduate from [Thammasat University](https://tu.ac.th/). Bachelor’s degree candidate in Computer Engineering.

[My Github profile](https://github.com/ItsRatcha)
