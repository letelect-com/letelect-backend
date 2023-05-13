from django.contrib.auth import authenticate
from management.models import Contact, User
from rest_framework import serializers
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return Response(user, status=200)
        raise Response(
            {"error": "Unable to log in with provided credentials."}, status=400)


class RegisterClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('fullname', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            fullname=validated_data['fullname'],
        )
        return user


class RegisterStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('fullname', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_superuser(
            email=validated_data['email'],
            password=validated_data['password'],
            fullname=validated_data['fullname'],
        )
        return user


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = ('created_at',)

    def create(self, validated_data):
        contact = Contact.objects.create(
            fullname=validated_data['fullname'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            message=validated_data['message'],
        )
        return contact
