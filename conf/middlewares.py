from django.contrib.auth import authenticate


class AutoAuthAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if not request.user.is_authenticated and "login" not in request.path:
            user = authenticate(request, username="admin", password="password")
            request.user = user

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
