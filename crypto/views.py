from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Prefetch
from .permissions import OrganizationSpecificAccess
from .models import CryptoPrice
from .serializers import CryptoPriceSerializer
from .pagination import NestedPricesPagination


class CryptoPriceViewSet(viewsets.ModelViewSet):
    serializer_class = CryptoPriceSerializer
    permission_classes = [OrganizationSpecificAccess]
    pagination_class = NestedPricesPagination

    def get_queryset(self):
        user_organizations = self.request.user.organizations.all()
        return CryptoPrice.objects.filter(org_id__in=user_organizations)

    def list(self, request, *args, **kwargs):
        user_organizations = request.user.organizations.prefetch_related(
            Prefetch(
                'crypto_prices',
                queryset=CryptoPrice.objects.order_by('-timestamp')
            )
        ).order_by('name')

        paginator = self.pagination_class()
        data = {}

        for org in user_organizations:
            prices = org.crypto_prices.all()
            paginated_prices = paginator.paginate_prices(prices, request)
            pagination_data = paginator.get_prices_pagination_data()

            data[str(org.id)] = {
                'name': org.name,
                'prices': CryptoPriceSerializer(paginated_prices, many=True).data,
                'prices_pagination': pagination_data
            }

        return Response(data)

    def perform_create(self, serializer):
        org_id = self.request.data.get('org_id')

        if org_id:
            if not self.request.user.organizations.filter(id=org_id).exists():
                return Response(
                    {"error": "User does not belong to this organization"},
                    status=status.HTTP_403_FORBIDDEN
                )
            org = self.request.user.organizations.get(id=org_id)
        else:
            if not self.request.user.organizations.exists():
                return Response(
                    {"error": "User must belong to at least one organization"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            org = self.request.user.organizations.first()

        serializer.save(org_id=org)
