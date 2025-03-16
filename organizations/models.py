from django.contrib.auth.models import User
from django.db import models
import uuid


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_organizations")
    members = models.ManyToManyField(
        User, related_name="organizations", blank=True)  # New field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
