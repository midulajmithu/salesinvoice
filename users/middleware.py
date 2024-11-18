from django.shortcuts import redirect
from django.urls import reverse

class RestrictBackMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if user is trying to access a restricted page after logging out
        if not request.user.is_authenticated and request.path not in [reverse('sign_in'), reverse('sign_up')]:
            return redirect('sign_in')  # Redirect to your login page

        return response