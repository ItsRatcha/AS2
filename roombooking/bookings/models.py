from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ValidationError

DAY_CHOICES = [
    (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'),
    (3, 'Thursday'), (4, 'Friday'),
]

TIME_CHOICES = [
    (9, '09:00'), (10, '10:00'), (11, '11:00'), (12, '12:00'),
    (13, '13:00'), (14, '14:00'), (15, '15:00'), (16, '16:00'), (17, '17:00'),
]


class Day(models.Model):
    day_of_week = models.IntegerField(choices=DAY_CHOICES, unique=True)
    def __str__(self):
        return self.get_day_of_week_display()
    class Meta:
        ordering = ['day_of_week']

class TimeSlot(models.Model):
    time = models.IntegerField(choices=TIME_CHOICES, unique=True)
    def __str__(self):
        return self.get_time_display()
    class Meta:
        ordering = ['time']


# --- Main Models ---

class Room(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    status = models.BooleanField(default=True)
    image_url = models.URLField(
        max_length=500,
        blank=True,
        default="https://i.ibb.co/W4Bjq1tG/elementor-placeholder-image.jpg"
    )
    def __str__(self):
        return self.name

# Step 2: Create the central RoomRestriction model
class RoomRestriction(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="restrictions")
    day = models.ForeignKey(Day, on_delete=models.CASCADE, null=True, blank=True)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        if self.day is None and self.time_slot is None:
            raise ValidationError("A restriction must specify at least a day or a time slot.")

    def __str__(self):
        if self.day and self.time_slot:
            return f"{self.room.name} restricted on {self.day} at {self.time_slot}"
        elif self.day:
            return f"{self.room.name} restricted all day on {self.day}s"
        elif self.time_slot:
            return f"{self.room.name} restricted every day at {self.time_slot}"
        return f"Invalid restriction for {self.room.name}"
    
    class Meta:
        unique_together = ('room', 'day', 'time_slot')


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.IntegerField(choices=TIME_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def clean(self):
        if not self.room:
            super().clean()
            return
            
        is_restricted = RoomRestriction.objects.filter(
            Q(room=self.room) & (
                Q(day__day_of_week=self.day, time_slot__isnull=True) |
                Q(day__isnull=True, time_slot__time=self.start_time) |
                Q(day__day_of_week=self.day, time_slot__time=self.start_time)
            )
        ).exists()

        if is_restricted:
            raise ValidationError(
                f"{self.room.name} is not available at {self.get_start_time_display()} on {self.get_day_display()}s."
            )

        existing_bookings = Booking.objects.filter(
            room=self.room, day=self.day, start_time=self.start_time
        ).exclude(pk=self.pk)
            
        if existing_bookings.exists():
            raise ValidationError("This room is already booked for this time slot.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking for {self.room.name} on {self.get_day_display()} at {self.get_start_time_display()} by {getattr(self.user, 'username', 'Unknown')}"