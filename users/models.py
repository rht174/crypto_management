from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    organizations = models.ManyToManyField(
        'organizations.Organization',
        related_name='member_users',
        blank=True
    )

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username
