from rest_framework.routers import DefaultRouter
from .views import OrganizationViewSet

router = DefaultRouter()
router.register('orgs', OrganizationViewSet, basename='organization')

urlpatterns = router.urls
