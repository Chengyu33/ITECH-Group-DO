from django.contrib import admin
from .models import Student, Administrator, Event, Registration
# Register your models here.

admin.site.register(Student)
admin.site.register(Administrator)
admin.site.register(Event)
admin.site.register(Registration)