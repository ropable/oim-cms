from rest_framework.viewsets import ReadOnlyModelViewSet

from tracking.models import DepartmentUser
from tracking.serializers import DepartmentUserSerializer


class DepartmentUserViewSet(ReadOnlyModelViewSet):
    queryset = DepartmentUser.objects.all()
    serializer_class = DepartmentUserSerializer
