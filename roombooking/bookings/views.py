from django.shortcuts import render, redirect, get_object_or_404
from .forms import CheckBookingForm
from .models import Booking, Room
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, 'bookings/index.html', {
        'title': 'Home',
        'rooms': Room.objects.all()
    })
def my_bookings(request):
    if not request.user.is_authenticated:
        return redirect('index')
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/my_bookings.html', {
        'title': 'My Bookings',
        'bookings': bookings
    })

def check_booking(request):
    message = ""
    selected_room = request.GET.get('room', None)
    selected_day = request.GET.get('day', None)
    selected_time = request.GET.get('start_time', None)
    rooms = Room.objects.all()
    show_booking_button = False
    if 'room' in request.GET:
        form = CheckBookingForm(request.GET)
        if form.is_valid():
            room = form.cleaned_data['room']
            day = form.cleaned_data['day']
            start_time = form.cleaned_data['start_time']

            bookings = Booking.objects.filter(
                room=room,
                day=day,
                start_time=start_time
            )
            

            if bookings.exists():
                message = "The room is not available for the selected time."
            else:
                message = "The room is available for the selected time."
                show_booking_button = True
        else:
            message = "Invalid input. Please correct the errors below."
        
        context = {
        'title': 'Home',
        'rooms': Room.objects.all(),
        'booking_status': message,
        'show_booking_button': show_booking_button,
        'selected_room': selected_room,
        'selected_day': selected_day,
        'selected_time': selected_time,
        }
        return render(request, 'bookings/index.html', context)
    
@require_POST
def create_booking(request):
    room_id = request.POST.get('room_id')
    day = request.POST.get('day')
    start_time = request.POST.get('start_time')

    if not request.user.is_staff:
        existing = Booking.objects.filter(user=request.user)
        if existing:
            messages.error(request,"You can only have one booking at a time")
            return redirect('index')
    try:
        room = Room.objects.get(id=room_id)
        booking = Booking(room=room, day=day, start_time=start_time, user=request.user)
        booking.save()
        return redirect('my_bookings')
    except Room.DoesNotExist:
        return redirect('index')

def cancel_booking(request, booking_id):
    if not request.user.is_authenticated:
        return redirect('index')
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
        booking.delete()
        return redirect('my_bookings')
    except Booking.DoesNotExist:
        return redirect('my_bookings')

def rooms(request):
    return render(request, 'bookings/rooms.html', {'rooms': Room.objects.all()})


def room_detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    # time slots (9–17)
    time_choices = dict(Booking._meta.get_field("start_time").choices)
    # days (Mon–Fri)
    day_choices = dict(Booking._meta.get_field("day").choices)

    # grab all bookings for this room
    bookings = Booking.objects.filter(room=room)

    # build availability grid
    availability = []
    for day_val, day_name in day_choices.items():
        day_slots = []
        for time_val, time_label in time_choices.items():
            booked = bookings.filter(day=day_val, start_time=time_val).first()
            day_slots.append({
                "time": time_label,
                "booked": bool(booked),
                "user": booked.user.username if booked else None
            })
        availability.append({
            "day": day_name,
            "slots": day_slots
        })

    return render(request, "bookings/room_detail.html", {
        "room": room,
        "availability": availability
    })