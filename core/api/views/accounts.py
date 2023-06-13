from rest_framework.views import APIView
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from api.serializers import ContactSerializer, RegisterClientSerializer, RegisterStaffSerializer, UserSerializer
from management.models import Contact, User


class TestAPI(APIView):
    def get(self, request):
        return Response({
            'greet': 'Hello, world!',
            'endpoints': '/api/test/',
            'message': 'The LetElect API is up and running!',
        })


class LoginAPI(KnoxLoginView):
    '''Login api endpoint'''
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class SignUpClientAPI(generics.GenericAPIView):
    '''This CBV is used to register a new CLIENT user - CLIENT SIGN-UP'''
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterClientSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1],
        }, status=status.HTTP_201_CREATED)


class RegisterStaffAPI(generics.GenericAPIView):
    '''This CBV is used to register a new STAFF user'''
    permission_classes = [permissions.IsAdminUser]
    serializer_class = RegisterStaffSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1],
        }, status=status.HTTP_201_CREATED)


class ChangePasswordAPI(APIView):
    '''This CBV is used to change a user's password'''
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        user = request.user
        new_password = request.data.get('new_password')
        if new_password:
            user.set_password(new_password)
            user.save()
            return Response({
                "message": "Password Changed Successfully",
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Invalid Password Length!",
            }, status=status.HTTP_400_BAD_REQUEST)


class VotersListAPI(APIView):
    '''This CBV is used to get all voters'''
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        user = request.user
        election_id = request.data.get('election_id')
        if user.is_superuser:
            voters = User.objects.filter(is_voter=False).order_by('-created_at')  # noqa
        else:
            voters = User.objects.filter(is_voter=False, election_id=election_id).order_by('-created_at')  # noqa
        serializer = UserSerializer(voters, many=True)
        return Response({
            "voters": serializer.data,
        }, status=status.HTTP_200_OK)


class CreateUpdateVoterAPI(APIView):
    '''CBV to create and update voters - voters are user objects'''
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        return Response({
            "message": "Voter Created Successfully!",
        }, status=status.HTTP_201_CREATED)


class UserProfileAPI(APIView):
    '''This CBV is used to get a user's profile'''
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({
            "user": UserSerializer(user).data,
        }, status=status.HTTP_200_OK)


class ContactUsAPI(APIView):
    '''This CBV is used to send a message to the admin'''
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        '''used to send a message to the admin via the contact form'''
        # serializer = ContactSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # contact = serializer.save()
        contact = Contact.objects.create(
            name=request.data.get('name'),
            phone=request.data.get('phone'),
            email=request.data.get('email'),
            message=request.data.get('message'),
        )
        return Response({
            "message": "Message Sent Successfully!",
        }, status=status.HTTP_200_OK)


class ContactUsListAPI(APIView):
    '''This CBV is used to get all messages sent to the admin'''
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        contacts = Contact.objects.all().order_by('-created_at')
        serializer = ContactSerializer(contacts, many=True)
        return Response({
            "contacts": serializer.data,
        }, status=status.HTTP_200_OK)
