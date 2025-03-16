from rest_framework import viewsets, permissions
from .models import CryptoPrice
from .serializers import CryptoPriceSerializer


class CryptoPriceViewSet(viewsets.ModelViewSet):
    serializer_class = CryptoPriceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see their org's crypto data
        return CryptoPrice.objects.filter(org__owner=self.request.user)
