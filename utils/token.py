from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import urllib.parse

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token serializer to add extra user data to the JWT payload.
    """
    @classmethod
    def get_token(cls, user):
        # Get the default token payload
        token = super().get_token(user)

        # Add custom claims
        token['is_superuser'] = user.is_superuser
        token['username'] = user.username

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to use the custom token serializer.
    """
    serializer_class = MyTokenObtainPairSerializer


@login_required
def exchange_token(request):
    # This view is hit after the user has successfully logged in via social auth
    # The `request.user` is now populated by the social_django backend.
    
    # Generate a JWT for the user using our custom serializer to include custom claims
    refresh = MyTokenObtainPairSerializer.get_token(request.user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    # URL encode the tokens to safely pass them as query parameters
    params = urllib.parse.urlencode({
        'access': access_token,
        'refresh': refresh_token,
    })
    
    # Redirect back to the React app with the tokens in the URL
    # In a real production app, you might use a more secure method
    # like setting HttpOnly cookies.
    return redirect(f'{settings.MY_FRONTEND_HOST}/social-auth-callback?{params}')