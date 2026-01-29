from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema

from .models import User
from .serializers import UserSerializer, RegisterSerializer
from .services import UserCacheService


class UserListView(APIView):
    @swagger_auto_schema(responses={200: UserSerializer(many=True)})
    def get(self, request):
        cached = UserCacheService.get_users_list()
        if cached:
            return Response(cached)
        
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        UserCacheService.set_users_list(serializer.data)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UserSerializer, responses={201: UserSerializer})
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            UserCacheService.invalidate()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    @swagger_auto_schema(responses={200: UserSerializer})
    def get(self, request, pk):
        cached = UserCacheService.get_user(pk)
        if cached:
            return Response(cached)
        
        user = self.get_object(pk)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user)
        UserCacheService.set_user(pk, serializer.data)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UserSerializer, responses={200: UserSerializer})
    def put(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            UserCacheService.invalidate_user(pk)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=UserSerializer, responses={200: UserSerializer})
    def patch(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            UserCacheService.invalidate_user(pk)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user.delete()
        UserCacheService.invalidate_user(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer, responses={201: UserSerializer})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            UserCacheService.invalidate()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)