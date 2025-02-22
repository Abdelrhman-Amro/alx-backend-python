from datetime import datetime


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        time_now = datetime.now()
        user = request.user
        path = request.path
        log = f"{time_now} - User: {user} - Path: {path}\n"

        with open("requests.log", "r+") as f:
            content = f.read()
            f.seek(0, 0)  # info: this is used to reset the cursor
            f.write(log + content)

        response = self.get_response(request)

        return response
