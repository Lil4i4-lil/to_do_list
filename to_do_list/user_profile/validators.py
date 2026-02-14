from django.core.exceptions import ValidationError
import re


def validate_name(name: str) -> None:
    pattern = r'^[а-яА-Яa-zA-Z\-\']+$'

    if not re.match(pattern, name):
        raise ValidationError(
            'Имя должно содержать только буквы, знак "-" или знак "\'"'
        )