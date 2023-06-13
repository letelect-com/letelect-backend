from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, permissions

from management.models import Candidate
from api.serializers import CandidateSerializer


class CandidateListAPI(APIView):
    '''CBV to list all candidates'''

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        candidates = Candidate.objects.all()
        return Response({
            'candidates': CandidateSerializer(CandidateSerializer, many=True).data,
        }, status=status.HTTP_200_OK)
