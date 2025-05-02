class ForceHTTPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Force HTTP protocol
        request.META['wsgi.url_scheme'] = 'http'
        
        response = self.get_response(request)
        
        return response
