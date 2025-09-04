from django import forms
from django.core.exceptions import ValidationError
from .models import Booking

class BookingAdminForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)  # fields are now initialized

        # assign the user for validation
        if self.request and not self.instance.pk:
            self.instance.user = self.request.user

        # make room/day/start_time required
        self.fields['room'].required = True
        self.fields['day'].required = True
        self.fields['start_time'].required = True

    def clean(self):
        cleaned_data = super().clean()
        user = self.instance.user
        room = cleaned_data.get('room')
        day = cleaned_data.get('day')
        start_time = cleaned_data.get('start_time')

        # room double booking
        qs_room = Booking.objects.filter(room=room, day=day, start_time=start_time)
        if self.instance.pk:
            qs_room = qs_room.exclude(pk=self.instance.pk)
        if qs_room.exists():
            raise ValidationError({'__all__': "Room is already booked for this time slot"})

        # single booking per user
        qs_user = Booking.objects.filter(user=user)
        if self.instance.pk:
            qs_user = qs_user.exclude(pk=self.instance.pk)
        if qs_user.exists():
            raise ValidationError({'__all__': "You can only have one booking at a time"})

        return cleaned_data
