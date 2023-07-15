import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_username(value):
    if value == 'me':
        raise ValidationError('Имя пользователя не может быть "me".')
    # Удаление всех валидных символов из полученного значения
    invalid_chars = re.sub(r'[a-zA-Z0-9-_\.]', '', value)
    if invalid_chars:
        raise ValidationError(
            f'Не допустимые символы "{invalid_chars}" в нике.')


def validate_year(value):
    now = timezone.now().year
    if value > now:
        raise ValidationError(
            f'{value} не может быть больше {now}'
        )
