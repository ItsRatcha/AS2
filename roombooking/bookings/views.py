from django.shortcuts import render, redirect, get_object_or_404
from .forms import CheckBookingForm
from .models import Booking, Room, RoomRestriction
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages


def is_slot_restricted(room, day, start_time):
    return RoomRestriction.objects.filter(
        Q(room=room) & (
            Q(day__day_of_week=day, time_slot__isnull=True) |
            Q(day__isnull=True, time_slot__time=start_time) |
            Q(day__day_of_week=day, time_slot__time=start_time)
        )
    ).exists()


# --- Views ---

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

            if not room.status:
                message = "The room is currently under maintenance."
            elif is_slot_restricted(room, day, start_time):
                message = "The room is unavailable at the selected time due to restrictions."
            elif Booking.objects.filter(room=room, day=day, start_time=start_time).exists():
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

    # Basic validation
    if not all([room_id, day, start_time]):
        messages.error(request, "Missing information. Please try again.")
        return redirect('index')

    try:
        room = Room.objects.get(id=room_id)
        day_int = int(day)
        start_time_int = int(start_time)

        if not room.status:
            messages.error(request, f"{room.name} is currently under maintenance.")
            return redirect('index')

        if is_slot_restricted(room, day_int, start_time_int):
            messages.error(request, f"{room.name} is unavailable at the selected time.")
            return redirect('index')

        if Booking.objects.filter(room=room, day=day_int, start_time=start_time_int).exists():
            messages.error(request, f"{room.name} is already booked for this slot.")
            return redirect('index')
        
        if not request.user.is_staff and Booking.objects.filter(user=request.user).exists():
            messages.error(request, "You can only have one booking at a time.")
            return redirect('index')
        
        booking = Booking(room=room, day=day_int, start_time=start_time_int, user=request.user)
        booking.save()
        messages.success(request, "Your booking was successful!")
        return redirect('my_bookings')

    except Room.DoesNotExist:
        messages.error(request, "The selected room does not exist.")
        return redirect('index')
    except (ValueError, TypeError):
        messages.error(request, "Invalid data submitted.")
        return redirect('index')


def cancel_booking(request, booking_id):
    if not request.user.is_authenticated:
        return redirect('index')
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    messages.success(request, "Your booking has been cancelled.")
    return redirect('my_bookings')

def rooms(request):
    return render(request, 'bookings/rooms.html', {'rooms': Room.objects.all()})

def room_detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    time_choices = dict(Booking._meta.get_field("start_time").choices)
    day_choices = dict(Booking._meta.get_field("day").choices)

    bookings = Booking.objects.filter(room=room)
    restrictions = RoomRestriction.objects.filter(room=room)
    
    restricted_slots = set()
    for r in restrictions:
        day = r.day.day_of_week if r.day else None
        time = r.time_slot.time if r.time_slot else None
        restricted_slots.add((day, time))

    availability = []
    for day_val, day_name in day_choices.items():
        day_slots = []
        for time_val, time_label in time_choices.items():
            booked = bookings.filter(day=day_val, start_time=time_val).first()

            is_restricted = (
                (day_val, None) in restricted_slots or
                (None, time_val) in restricted_slots or
                (day_val, time_val) in restricted_slots
            )
            
            day_slots.append({
                "time": time_label,
                "booked": bool(booked),
                "restricted": is_restricted,
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