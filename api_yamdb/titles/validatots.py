from django.utils import timezone
from django.core.exceptions import ValidationError


def year_of_creation_validator(value):
    if not (0 < value <= timezone.now().year):
        raise ValidationError('Год произведения должен быть не больше текущего')