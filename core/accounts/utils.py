import jwt
import datetime
from django.conf import settings
from django.utils import timezone
from .models import UserV2


def generate_jwt_tokens(user_v2_instance):
    """
    Manually generates both JWT access and refresh tokens for the given UserV2 instance.

    Args:
        user_v2_instance (UserV2): The UserV2 instance for which the JWT tokens are generated.

    Returns:
        dict: A dictionary containing the access and refresh tokens.
    """
    if not isinstance(user_v2_instance, UserV2):
        raise ValueError("The provided instance is not of type UserV2")

    # Ensure the user is active before generating the token
    if not user_v2_instance.is_active:
        raise ValueError("The user is not active. Cannot generate token.")

    # Define the JWT payload (access token)
    payload_access = {
        "user_id": user_v2_instance.id,
        "phone_number": user_v2_instance.phone_number,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(minutes=15),  # Token expires in 15 minutes
        "iat": datetime.datetime.utcnow(),  # Issued at time
    }

    # Define the JWT payload (refresh token)
    payload_refresh = {
        "user_id": user_v2_instance.id,
        "phone_number": user_v2_instance.phone_number,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(days=7),  # Refresh token expires in 7 days
        "iat": datetime.datetime.utcnow(),
    }

    # Secret key for encoding the JWT
    secret_key = (
        settings.SECRET_KEY
    )  # Make sure to use your Django SECRET_KEY or a custom one

    # Create the JWT access token
    access_token = jwt.encode(
        payload_access, secret_key, algorithm="HS256"
    )  # Using HMAC SHA-256 for signing

    # Create the JWT refresh token
    refresh_token = jwt.encode(
        payload_refresh, secret_key, algorithm="HS256"
    )  # Using HMAC SHA-256 for signing

    return {
        "access_token": str(access_token),  # Return access token as string
        "refresh_token": str(refresh_token),  # Return refresh token as string
    }
