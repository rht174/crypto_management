from rest_framework import serializers
from .models import CryptoPrice
from organizations.models import Organization


class CryptoPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoPrice
        fields = ["id", "org_id", "symbol", "price", "timestamp"]


class OrganizationCryptoPriceSerializer(serializers.ModelSerializer):
    prices = CryptoPriceSerializer(many=True, source='crypto_prices')

    class Meta:
        model = Organization
        fields = ('id', 'name', 'prices')
