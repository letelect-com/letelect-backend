from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, permissions

from management.models import Election
from api.serializers import ElectionSerializer


class ElectionsListAPI(APIView):
    '''CBV to list all elections'''

    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            elections = Election.objects.all().order_by('created_at')
        else:
            elections = Election.objects.filter(admin=request.user)

        return Response({
            'elections': ElectionSerializer(elections, many=True).data,
        }, status=status.HTTP_200_OK)
