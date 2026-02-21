from django.db import models
class OtpStatus(models.TextChoices):
    IN_PROGRESS = 'in_progress', 'In Progress'
    VERIFIED = 'verified', 'Verified'
    EXPIRED = 'expired', 'Expired'
    FAILED = 'failed', 'Failed'


class OtpTypes(models.TextChoices):
    EMAIL = 'email', 'Email'
    SMS = 'sms', 'SMS'
    APP = 'app', 'App'


class OtpFunction(models.TextChoices):
    REGISTER = 'register', 'Register'
    RESET_PASSWORD = 'reset_password', 'Reset Password'
    TWO_FACTOR_AUTH = 'two_factor_auth', 'Two-Factor Authentication'
    LOGIN = 'login', 'Login'
