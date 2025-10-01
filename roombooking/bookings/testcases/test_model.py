from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Room, Booking, Day, TimeSlot, RoomRestriction
from django.core.exceptions import ValidationError


User = get_user_model()

class TestRoomModel(TestCase):
    # Checks that the string representation of a Room object returns its name.
    def test_room_str(self):
        room = Room.objects.create(name="room A", capacity=10)
        self.assertEqual(str(room), "room A")


class TestDayAndTimeSlot(TestCase):
    # Check that Day and TimeSlot models return correct string representations and are ordered properly.
    def test_day_str_and_ordering(self):
        d1 = Day.objects.create(day_of_week=0)  # Monday
        d2 = Day.objects.create(day_of_week=2)  # Wednesday
        self.assertEqual(str(d1), "Monday")
        self.assertEqual(str(d2), "Wednesday")
        self.assertEqual(list(Day.objects.all()), [d1, d2])  # ordered by day_of_week

    def test_time_slot_str_and_ordering(self):
        t1 = TimeSlot.objects.create(time=9)
        t2 = TimeSlot.objects.create(time=11)
        self.assertEqual(str(t1), "09:00")
        self.assertEqual(str(t2), "11:00")
        self.assertEqual(list(TimeSlot.objects.all()), [t1, t2])  # ordered by time


class TestRoomRestriction(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="Conference C", capacity=25)

    def test_restriction_requires_day_or_time(self):
        # A restriction must specify at least a day or a time slot.
        restriction = RoomRestriction(room=self.room)
        with self.assertRaises(ValidationError):
            restriction.clean()

    def test_restriction_str_with_day_and_time(self):
        # A restriction must specify at least a day or a time slot.
        day = Day.objects.create(day_of_week=1)  # Tuesday
        slot = TimeSlot.objects.create(time=10)
        r = RoomRestriction.objects.create(room=self.room, day=day, time_slot=slot)
        self.assertIn("Tuesday", str(r))
        self.assertIn("10:00", str(r))

    def test_unique_together(self):
        # Ensure that the combination of room, day, and time_slot is unique.
        day = Day.objects.create(day_of_week=3)  # Thursday
        slot = TimeSlot.objects.create(time=14)
        RoomRestriction.objects.create(room=self.room, day=day, time_slot=slot)
        with self.assertRaises(Exception):  # IntegrityError
            RoomRestriction.objects.create(room=self.room, day=day, time_slot=slot)


class TestBooking(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="tester1", password="12345")
        self.user2 = User.objects.create_user(username="tester2", password="12345")
        self.room = Room.objects.create(name="Conference D", capacity=30)
        self.day = 0  # Monday
        self.slot = 9  # 09:00

    def test_booking_str(self):
        # The string representation of a Booking object should include the room name, day, and start time.
        booking = Booking.objects.create(
            room=self.room,
            day=self.day,
            start_time=self.slot,
            user=self.user1
        )
        self.assertIn("Conference D", str(booking))
        self.assertIn("Monday", str(booking))
        self.assertIn("09:00", str(booking))

    def test_double_booking_not_allowed(self):
        # Ensure that double booking the same room at the same time is not allowed.
        Booking.objects.create(
            room=self.room,
            day=self.day,
            start_time=self.slot,
            user=self.user1
        )
        booking2 = Booking(
            room=self.room,
            day=self.day,
            start_time=self.slot,
            user=self.user2
        )
        with self.assertRaises(ValidationError):
            booking2.full_clean()

    def test_booking_restricted(self):
        # Ensure that a booking cannot be made if a restriction exists for that room, day, and time slot.
        day_obj = Day.objects.create(day_of_week=self.day)
        slot_obj = TimeSlot.objects.create(time=self.slot)
        RoomRestriction.objects.create(room=self.room, day=day_obj, time_slot=slot_obj)

        booking = Booking(
            room=self.room,
            day=self.day,
            start_time=self.slot,
            user=self.user1
        )
        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_valid_booking_when_no_restriction(self):
        # A booking should be valid if no restrictions exist for that room, day, and time slot.
        booking = Booking.objects.create(
            room=self.room,
            day=self.day,
            start_time=self.slot,
            user=self.user1
        )
        self.assertEqual(Booking.objects.count(), 1)