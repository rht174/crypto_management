from rest_framework import viewsets, permissions
from .models import CryptoPrice
from .serializers import CryptoPriceSerializer


class CryptoPriceViewSet(viewsets.ModelViewSet):
    serializer_class = CryptoPriceSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CryptoPrice.objects.all()

    def get_queryset(self):
        return CryptoPrice.objects.filter(org_id__owner=self.request.user)
