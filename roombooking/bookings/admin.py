from django.contrib import admin
from .models import Booking, Room
from .forms import BookingAdminForm

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    form = BookingAdminForm
    exclude = ('user',)

    def get_form(self, request, obj=None, **kwargs):
        form_class = super().get_form(request, obj, **kwargs)
        # attach request to the form properly
        class FormWithRequest(form_class):
            def __new__(cls, *args, **kwargs2):
                kwargs2['request'] = request
                return form_class(*args, **kwargs2)
        return FormWithRequest

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)
