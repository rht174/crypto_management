from rest_framework import serializers
from django.contrib.auth import get_user_model
from organizations.models import Organization
from organizations.serializers import OrganizationSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    organizations = OrganizationSerializer(many=True, read_only=True)
    organization_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password',
                  'organizations', 'organization_ids')
        read_only_fields = ('id', 'organizations')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        organization_ids = validated_data.pop('organization_ids', [])

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )

        if organization_ids:
            organizations = Organization.objects.filter(
                id__in=organization_ids)
            user.organizations.add(*organizations)

        return user

    def update(self, instance, validated_data):
        organization_ids = validated_data.pop('organization_ids', None)

        for attr, value in validated_data.items():
            if attr != 'password':
                setattr(instance, attr, value)

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        if organization_ids is not None:
            organizations = Organization.objects.filter(
                id__in=organization_ids)
            instance.organizations.set(organizations)

        instance.save()
        return instance
