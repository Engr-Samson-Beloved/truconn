from django.urls import path 
from .views import ConsentApiView, UserConsentView, CitizenTransparencyLog


urlpatterns = [
    path('consents/', ConsentApiView.as_view()),
    path('consents/<int:consent_id>/toggle/', UserConsentView.as_view()),
    path('consents/transparency-log/', CitizenTransparencyLog.as_view())
]