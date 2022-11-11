from django.contrib import admin

from .models import (
    UserSession,
    TimeFrame,
    Screenshot
)

admin.site.register(UserSession)
admin.site.register(TimeFrame)
admin.site.register(Screenshot)
