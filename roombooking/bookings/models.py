from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

# Create your models here.
class Room(models.Model):

    name = models.CharField(max_length=100)
    capacity = models.IntegerField(max_length=500)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Booking(models.Model):

    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False, blank=False)
    date = models.IntegerField(choices=[(0, 'Monday'),(1, 'Tuesday'),(2, 'Wednesday'),(3, 'Thursday'),(4, 'Friday'),], null=False, blank=False)
    start_time = models.IntegerField(choices=[(9, '09:00'),(10, '10:00'),(11, '11:00'),(12, '12:00'),(13, '13:00'),(14, '14:00'),(15, '15:00'),(16, '16:00'),(17, '17:00'),], null=False, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def clean(self):
        # Check for double bookings
        existing_bookings = Booking.objects.filter(room=self.room, day=self.day, start_time=self.start_time)
        if existing_bookings.exists():
            raise ValidationError("Room is already booked for this time slot")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Room_{self.room.name}_{self.get_day_display()}_{self.start_time}_{getattr(self.user, 'username', 'Unknown')}"
    