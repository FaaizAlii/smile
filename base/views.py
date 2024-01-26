from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import APIView, api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework import generics

from .serializers import *
# Create your views here.

class list_urls(generics.ListAPIView):
    def get(self, request):
        data = {
            'list urls':'list-url/',
            'login - done':'login/',
            'signup - done':'signup/',
            'logout - done':'logout/',
            'step1 - done':'complete/step1/',
            'step2 - done':'complete/step2/',
            'step3 - done':'complete/step3/',
            'my account':"my_account/",
            'dashboard':'dashboard/',
            'goals':'goals/',
            'tutorial':'tutorial/',
            'messaging':'messaging/',
            'friends':'friends/',
            'notifications':'notifications/',
            'stats':'stats/',
            'activities':'activities/',
            'level':'level/',
            'community':'community/',
            'social-section':'social-section/',
        }
        return Response(data, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)

            response_data = {
                'email': email,
                'token': token.key
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()

        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)


# class Profile1View(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
    
#     def post(self, request):
#         serializer = Profile1Serializer(data=request.data, partial=True)
#         if serializer.is_valid():
#             profile = serializer.save(user = self.request.user)

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class Profile2View(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
    
#     def post(self, request):
#         try:
#             profile = Profile.objects.get(user=request.user)
#         except Profile.DoesNotExist:
#             profile = None
#         if profile:
#             serializer = Profile2Serializer(instance=profile, data=request.data, partial=True, context={'request': request})
            
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"error":"no profile found"}, status=status.HTTP_404_NOT_FOUND)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def post(self, request):
        try:
            profile = Profile.objects.get(user=self.request.user)
            serializer = ProfileSerializer(instance=profile, data=request.data, partial=True)
        except Profile.DoesNotExist:
            serializer = ProfileSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            profile = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return Response({"error": "Profile does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(instance=profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class Profile3View(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def post(self, request):
        serializer = Profile3Serializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['user'] = self.request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        


class MyAccountView(APIView):
    def put(self, request):
        try:
            profile = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return Response({"error": "Profile does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(instance=profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        try:
            profile = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return Response({"error": "Profile does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)