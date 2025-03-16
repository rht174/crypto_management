from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CryptoPriceViewSet

router = DefaultRouter()
router.register('prices', CryptoPriceViewSet, basename='cryptoprice')

urlpatterns = router.urls
