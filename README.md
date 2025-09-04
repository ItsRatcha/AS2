# Room Booking Django web app
This is a roombooking web app that allows students to book rooms. This project is a part of an assignment for class CN331.

![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)
![Build Status](https://img.shields.io/badge/progress-25-brightgreen)

---

![placeholder for my web app screenshot](https://image.petmd.com/files/styles/863x625/public/CANS_dogsmiling_379727605.jpg)
*this is a placeholder for my screenshot


## Current feature
- [x] Create rooms
- [x] Create users with password
	- users still need to be add to student group manually
- [x] Any user can create a booking with room, day and time.
- [x] Students cannot book more than one booking at a time.
- [x] A room cannot have more than one user book it at the same time(no double booking)
- [ ] Booking with empty field(s) will cause an error pop up.
- [ ] Users can delete their own booking.
- [ ] Create a html page for user to check availability and booking form.
- [ ] Create a login-logout page.
- [ ] Use CSS to customize the page.
- [ ] Create a staff group (staffs and admin have unlimited booking and can delete bookings)

## How to run
1. Git clone the repository
2. `pip install -r requirements.txt`
3. `cd roombooking`
4. `python manage.py runserver`
