from django.contrib import admin
from .models import UserProfile, EmailDigest

admin.site.register(UserProfile)
admin.site.register(EmailDigest)