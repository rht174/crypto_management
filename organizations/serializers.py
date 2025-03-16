from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, required=False)

    class Meta:
        model = Organization
        fields = ["id", "name", "owner", "members", "created_at"]
        read_only_fields = ["owner"]

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)
