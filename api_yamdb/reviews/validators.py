import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError('Имя пользователя не может быть "me".')
    invalid_chars = re.sub(r'[a-zA-Z0-9-_\.]', '', value)
    if invalid_chars:
        raise ValidationError(
            f'Не допустимые символы "{invalid_chars}" в нике.')
