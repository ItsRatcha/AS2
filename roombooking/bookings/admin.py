from django.contrib import admin
from .models import Booking, Room, Day, TimeSlot, RoomRestriction
from .forms import BookingAdminForm

class RoomRestrictionInline(admin.TabularInline):
    model = RoomRestriction
    extra = 1
    verbose_name = "Restriction Rule"
    verbose_name_plural = "Restriction Rules"

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'status')
    inlines = [RoomRestrictionInline]

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    form = BookingAdminForm
    exclude = ('user',)
    list_display = ('room', 'day', 'start_time', 'user')
    list_filter = ('day', 'room')

    def get_form(self, request, obj=None, **kwargs):
        form_class = super().get_form(request, obj, **kwargs)
        class FormWithRequest(form_class):
            def __new__(cls, *args, **kwargs2):
                kwargs2['request'] = request
                return form_class(*args, **kwargs2)
        return FormWithRequest

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Day)
admin.site.register(TimeSlot)