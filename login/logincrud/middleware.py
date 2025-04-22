from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_paths = [reverse('login'), '/static/', reverse('logout')]
        print("User details",request.user)
        print(f"[Middleware] Path: {request.path}, Authenticated: {request.user.is_authenticated}")

        if not request.user.is_authenticated:
            if not any(request.path.startswith(path) for path in allowed_paths):
                return redirect(reverse('login'))
        return self.get_response(request)

class DeleteCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the user has logged out
        if request.path == reverse('logout'):
            # Remove the 'access_token' cookie or any other cookies you want to delete
            response.delete_cookie('access_token', path='/')  # Adjust path if needed

        return response
