import time
import json
from django.utils.deprecation import MiddlewareMixin
from .models import AuditLog


class AuditMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._start_time = time.time()
        return None

    def process_response(self, request, response):
        try:
            # Calculate response time
            response_time = int((time.time() - getattr(request, '_start_time', time.time())) * 1000)
            
            # Get client IP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
            
            # Get request body for POST/PUT/PATCH
            request_body = None
            if request.method in ['POST', 'PUT', 'PATCH'] and hasattr(request, 'body'):
                try:
                    request_body = json.loads(request.body.decode('utf-8'))
                except:
                    request_body = None
            
            # Create audit log
            AuditLog.objects.create(
                user_id=None,  # Since we don't have authentication
                user_ip=ip,
                method=request.method,
                path=request.path,
                status_code=response.status_code,
                request_body=request_body,
                response_time_ms=response_time
            )
        except Exception as e:
            # Don't let logging errors break the response
            pass
        
        return response