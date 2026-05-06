from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from cookie_cutter.organizations.api.views import OrganizationViewSet
from cookie_cutter.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("organizations", OrganizationViewSet)


app_name = "api"
urlpatterns = router.urls
