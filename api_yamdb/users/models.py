from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
VALID_NAME = RegexValidator(r'^[\w.@+-]+\Z')


class User(AbstractUser):
    ROLES = {
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    }
    username = models.CharField(
        'Имя пользователя',
        validators=[VALID_NAME],
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        blank=True
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
    )
    role = models.CharField(
        'Разрешения пользователя',
        choices=ROLES,
        max_length=15,
        default=USER,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.username)

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER
