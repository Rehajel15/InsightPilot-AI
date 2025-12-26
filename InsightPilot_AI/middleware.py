class NgrokSkipWarningMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Add the header to skip the ngrok-warningpage
        response["ngrok-skip-browser-warning"] = "true"
        return response