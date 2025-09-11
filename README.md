# Room Booking Django web app
This is a roombooking web app that allows students to book rooms. This project is a part of an assignment for class CN331.

![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)
![Build Status](https://img.shields.io/badge/progress-25-brightgreen)

---
![title](Screenshots/Title.jpg)

## Current feature
- [x] Create rooms
- [x] Create users with password
	- users still need to be add to student group manually
- [x] Any user can create a booking with room, day and time.
- [x] Students cannot book more than one booking at a time.
- [x] A room cannot have more than one user book it at the same time(no double booking)
- [x] Users can delete their own booking.
- [x] Create a html page for user to check availability and booking form.
- [x] Create a login-logout page.
- [x] Use CSS to customize the page. (Tailwindcss)
- [x] Create a staff group (staffs and admin have unlimited booking and can delete bookings)
- [x] Jump to "my booking" page after book.
- [x] Users can only have one booking at a time.
- [x] Rooms page with placeholder image.
- [x] Tab icon.
- [x] Links to repo, contract and admin page at the bottom of sidebar.
- [x] Each room has its own page showing time available and have booking option.
- [x] Homepage have a slideshow of rooms
- [x] Status block to mark rooms as under maintenance.

## How to run
1. Git clone the repository
   1. (Optional) User virtual environment with `python -m venv .venv` and `.\.venv\Scripts\activate`
2. `pip install -r requirements.txt`
3. `cd roombooking`
4. `python manage.py tailwind dev`.
   You can use runserver, but will need a separate window for running Tailwind
   1. `python manage.py runserver`
   2. `python manage.py tailwind start`

## Screetshots
![screenshot1](Screenshots/Screenshot1.png)
![screenshot2](Screenshots/Screenshot2.png)
![screenshot3](Screenshots/Screenshot3.png)
![screenshot4](Screenshots/Screenshot4.png)