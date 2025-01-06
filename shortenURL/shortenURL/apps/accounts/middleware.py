# shortenURL/apps/accounts/middleware.py
import logging

logger = logging.getLogger('django')

class OAuthDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'callback' in request.path and ('facebook' in request.path or 'google' in request.path):
            logger.info(f"Pre-response: User authenticated: {request.user.is_authenticated}")
            logger.info(f"Pre-response: Session keys: {request.session.keys()}")
            
            response = self.get_response(request)
            
            logger.info(f"Post-response: Status: {response.status_code}")
            logger.info(f"Post-response: User authenticated: {request.user.is_authenticated}")
            logger.info(f"Post-response: Session keys: {request.session.keys()}")

            logger.info(f"Response Headers: {dict(response.headers)}")
            return response
        return self.get_response(request)