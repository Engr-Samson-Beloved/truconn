from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.conf import settings

def custom_exception_handler(exc, context):
    """
    Custom exception handler that ensures CORS headers are always present
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        request = context.get('request')
        origin = request.META.get('HTTP_ORIGIN', '') if request else ''
        
        # Check if origin is in allowed origins
        allowed_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', [])
        if origin in allowed_origins:
            response['Access-Control-Allow-Origin'] = origin
            response['Access-Control-Allow-Credentials'] = 'true'
            response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'accept, accept-encoding, authorization, content-type, dnt, origin, user-agent, x-csrftoken, x-requested-with'
    
    return response

