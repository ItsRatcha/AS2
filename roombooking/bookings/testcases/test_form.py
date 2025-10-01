# bookings/testcases/test_form.py

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from bookings.models import Room, Booking, Day, TimeSlot, RoomRestriction
from bookings.forms import BookingAdminForm, CheckBookingForm

User = get_user_model()

class BookingAdminFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.room1 = Room.objects.create(name='Conference Room A', capacity=10)
        cls.room2 = Room.objects.create(name='Conference Room B', capacity=8)
        cls.monday = Day.objects.create(day_of_week=0)
        cls.tuesday = Day.objects.create(day_of_week=1)
        cls.time_0900 = TimeSlot.objects.create(time=9)
        cls.time_1000 = TimeSlot.objects.create(time=10)
        cls.user1 = User.objects.create_user(username='user1', password='password')
        cls.user2 = User.objects.create_user(username='user2', password='password')
        cls.existing_booking = Booking.objects.create(
            user=cls.user1,
            room=cls.room1,
            day=0,
            start_time=9
        )
        cls.factory = RequestFactory()

    def test_form_is_valid_with_correct_data(self):
        request = self.factory.get('/')
        request.user = self.user2
        form_data = {
            'room': self.room1.pk,
            'day': 1,
            'start_time': 10,
            'user': self.user2.pk
        }
        form = BookingAdminForm(data=form_data, request=request)
        form.instance.user = self.user2
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_is_invalid_if_room_is_double_booked(self):
        request = self.factory.get('/')
        request.user = self.user2
        form_data = {
            'room': self.room1.pk,
            'day': 0,
            'start_time': 9,
            'user': self.user2.pk
        }
        form = BookingAdminForm(data=form_data, request=request)
        form.instance.user = self.user2

        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertEqual(form.errors['__all__'][0], "Room is already booked for this time slot")

    def test_form_is_invalid_if_user_already_has_booking(self):
        request = self.factory.get('/')
        request.user = self.user1
        form_data = {
            'room': self.room2.pk,
            'day': 2,
            'start_time': 11,
            'user': self.user1.pk
        }
        form = BookingAdminForm(data=form_data, request=request)
        form.instance.user = self.user1
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertEqual(form.errors['__all__'][0], "You can only have one booking at a time")

    def test_form_is_invalid_if_slot_is_restricted(self):
        RoomRestriction.objects.create(
            room=self.room2,
            day=self.tuesday,
            time_slot=self.time_1000
        )
        request = self.factory.get('/')
        request.user = self.user2
        form_data = {
            'room': self.room2.pk,
            'day': 1,
            'start_time': 10,
            'user': self.user2.pk
        }
        form = BookingAdminForm(data=form_data, request=request)
        form.instance.user = self.user2
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertIn("is not available at 10:00 on Tuesdays", form.errors['__all__'][0])

class CheckBookingFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.room = Room.objects.create(name='Test Room', capacity=5)

    def test_form_is_valid(self):
        form_data = {
            'room': self.room.pk,
            'day': 0,
            'start_time': 9
        }
        form = CheckBookingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_is_invalid_with_missing_data(self):
        form_data = {
            'room': self.room.pk,
            'day': 1,
        }
        form = CheckBookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('start_time', form.errors)

    def test_form_is_invalid_with_bad_choice(self):
        form_data = {
            'room': self.room.pk,
            'day': 10,
            'start_time': 9
        }
        form = CheckBookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('day', form.errors)