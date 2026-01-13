from django.contrib.auth.models import Group, Permission, User
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import GroupSerializer, PermissionSerializer, UserSerializer
from ..utils import can_access_financeiro


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.select_related("content_type").all()
    serializer_class = PermissionSerializer
    search_fields = ("name", "codename", "content_type__app_label")
    ordering_fields = ("name", "codename")


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.prefetch_related("permissions").all()
    serializer_class = GroupSerializer
    search_fields = ("name",)
    ordering_fields = ("name",)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.prefetch_related("groups", "user_permissions").all()
    serializer_class = UserSerializer
    search_fields = ("username", "first_name", "last_name", "email")
    ordering_fields = ("username", "email")


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_superuser": user.is_superuser,
            "groups": list(user.groups.values_list("name", flat=True)),
            "can_access_financeiro": can_access_financeiro(user),
        }
        return Response(data)
