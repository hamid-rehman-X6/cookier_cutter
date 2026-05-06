from rest_framework.viewsets import ModelViewSet
from cookie_cutter.organizations.models import Organization
from .serializers import OrganizationSerializer

class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer