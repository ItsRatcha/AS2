# bookings/testcases/test_views.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from bookings.models import Room, Booking, Day, TimeSlot, RoomRestriction

User = get_user_model()

class ViewsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.other_user = User.objects.create_user(username='otheruser', password='password')
        cls.staff_user = User.objects.create_user(username='staffuser', password='password', is_staff=True)

        cls.active_room = Room.objects.create(name='Active Room', capacity=10, status=True)
        cls.inactive_room = Room.objects.create(name='Inactive Room', capacity=5, status=False)
        
        cls.monday = Day.objects.create(day_of_week=0)
        cls.tuesday = Day.objects.create(day_of_week=1)
        cls.time_0900 = TimeSlot.objects.create(time=9)
        cls.time_1000 = TimeSlot.objects.create(time=10)

        cls.booking = Booking.objects.create(
            user=cls.user,
            room=cls.active_room,
            day=0,
            start_time=9,
        )
        
        RoomRestriction.objects.create(
            room=cls.active_room,
            day=cls.tuesday,
            time_slot=cls.time_1000
        )

    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/index.html')
        self.assertContains(response, self.active_room.name)

    def test_my_bookings_view_authenticated(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/my_bookings.html')
        self.assertContains(response, self.booking.room.name)
        self.assertEqual(len(response.context['bookings']), 1)

    def test_my_bookings_view_unauthenticated(self):
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        
    def test_check_booking_available(self):
        query_params = {
            'room': self.active_room.id,
            'day': 1,
            'start_time': 9,
        }
        response = self.client.get(reverse('check_booking'), query_params)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The room is available for the selected time.")
        self.assertTrue(response.context['show_booking_button'])

    def test_check_booking_unavailable_due_to_booking(self):
        query_params = {
            'room': self.active_room.id,
            'day': 0,
            'start_time': 9,
        }
        response = self.client.get(reverse('check_booking'), query_params)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The room is not available for the selected time.")
        self.assertFalse(response.context['show_booking_button'])

    def test_check_booking_unavailable_due_to_maintenance(self):
        query_params = {
            'room': self.inactive_room.id,
            'day': 0,
            'start_time': 9,
        }
        response = self.client.get(reverse('check_booking'), query_params)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The room is currently under maintenance.")
        self.assertFalse(response.context['show_booking_button'])

    def test_check_booking_unavailable_due_to_restriction(self):
        query_params = {
            'room': self.active_room.id,
            'day': 1,
            'start_time': 10,
        }
        response = self.client.get(reverse('check_booking'), query_params)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The room is unavailable at the selected time due to restrictions.")
        self.assertFalse(response.context['show_booking_button'])

    def test_create_booking_success(self):
        self.client.login(username='otheruser', password='password')
        post_data = {
            'room_id': self.active_room.id,
            'day': 1,
            'start_time': 9,
        }
        response = self.client.post(reverse('create_booking'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('my_bookings'))
        self.assertTrue(Booking.objects.filter(user=self.other_user).exists())

    def test_create_booking_fails_if_user_has_booking(self):
        self.client.login(username='testuser', password='password')
        post_data = {
            'room_id': self.active_room.id,
            'day': 1,
            'start_time': 9,
        }
        response = self.client.post(reverse('create_booking'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Booking.objects.filter(user=self.user).count(), 1)

    def test_create_booking_fails_if_slot_taken(self):
        self.client.login(username='otheruser', password='password')
        post_data = {
            'room_id': self.active_room.id,
            'day': 0,
            'start_time': 9,
        }
        response = self.client.post(reverse('create_booking'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        self.assertFalse(Booking.objects.filter(user=self.other_user).exists())

    def test_cancel_booking_success(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('cancel_booking', args=[self.booking.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('my_bookings'))
        self.assertFalse(Booking.objects.filter(id=self.booking.id).exists())

    def test_cancel_booking_fails_for_wrong_user(self):
        self.client.login(username='otheruser', password='password')
        response = self.client.get(reverse('cancel_booking', args=[self.booking.id]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Booking.objects.filter(id=self.booking.id).exists())
    
    def test_room_detail_view(self):
        response = self.client.get(reverse('room_detail', args=[self.active_room.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/room_detail.html')
        self.assertEqual(response.context['room'], self.active_room)
        
        availability = response.context['availability']
        monday_slots = availability[0]['slots']
        tuesday_slots = availability[1]['slots']
        
        self.assertTrue(monday_slots[0]['booked'])
        self.assertFalse(tuesday_slots[1]['booked'])
        self.assertTrue(tuesday_slots[1]['restricted'])