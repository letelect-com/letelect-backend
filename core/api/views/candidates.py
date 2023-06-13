from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, permissions

from management.models import Candidate, Election
from api.serializers import CandidateSerializer


class CandidateListAPI(APIView):
    '''CBV to list all candidates'''

    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            candidates = Candidate.objects.all().order_by('created_at')
        else:
            election_id = request.GET.get('election_id')
            election = Election.objects.filter(election_id=election_id).first()
            candidates = Candidate.objects.filter(position__election=election).order_by('created_at')  # noqa

        return Response({
            'candidates': CandidateSerializer(candidates, many=True).data,
        }, status=status.HTTP_200_OK)


class CreateUpdateCandidate(APIView):
    '''CBV to create and update candidate'''

    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        user = request.user
        # get particular election
        election_id = request.data.get('election_id')
        election = Election.objects.filter(election_id=election_id).first()
        # get candidate data: none if creating new candidate
        candidate_id = request.data.get('candidate_id')
        candidate = Candidate.objects.filter(candidate_id=candidate_id, position__election=election).first()  # noqa
        # get position data
        position_id = request.data.get('position_id')
        #
        if candidate is None:
            new_candidate = Candidate.objects.create(
                position=request.data.get('position'),
                fullname=request.data.get('fullname'),
                email=request.data.get('email'),
                phone=request.data.get('phone'),
                photo=request.data.get('photo'),
                election=election,
            )
            return Response({
                'message': "Candidate Created Successfully!",
                'candidate': CandidateSerializer(candidate).data,
            }, status=status.HTTP_200_OK)

        return Response({
            'candidate': CandidateSerializer(candidate).data,
        }, status=status.HTTP_200_OK)
