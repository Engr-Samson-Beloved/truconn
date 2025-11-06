from django.contrib import admin

from .models import Consent, UserConsent

admin.site.register(Consent)
admin.site.register(UserConsent)