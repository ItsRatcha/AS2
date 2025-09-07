from django.shortcuts import render
from .forms import CheckBookingForm
from .models import Booking, Room

# Create your views here.
def index(request):
    return render(request, 'bookings/index.html', {
        'title': 'Home',
        'rooms': Room.objects.all()
    })

def check_booking(request):
    message = ""
    rooms = Room.objects.all()
    if 'room' in request.GET:
        form = CheckBookingForm(request.GET)
        if form.is_valid():
            room = form.cleaned_data['room']
            date = form.cleaned_data['date']
            start_time = form.cleaned_data['start_time']

            bookings = Booking.objects.filter(
                room=room,
                date=date,
                start_time=start_time
            )
            

            if bookings.exists():
                message = "The room is not available for the selected time."
            else:
                message = "The room is available for the selected time."
        else:
            message = "Invalid input. Please correct the errors below."
        
        context = {
        'title': 'Home',
        'rooms': Room.objects.all(),
        'booking_status': message,
        }
        return render(request, 'bookings/index.html', context)