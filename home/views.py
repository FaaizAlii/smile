from random import randint
from  decimal import Decimal

from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import APIView, api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework import generics

from .serializers import *
from .models import *

# Create your views here.


def goal_setter(goal):
    if goal.smile_count == 0 and goal.smile_sec == 0:
        goal.smile_sec = randint(180, 480)
        goal.smile_count = randint(18, 30)
        goal.save()
        return goal


class DashBoardView(APIView):
    def get(self, request):
        try:
            user_serializer = UserSerializer(self.request.user)
            smile, _ = Smile.objects.get_or_create(user=self.request.user)
            level, _ = Level.objects.get_or_create(user=self.request.user)
            goal, _ = Goal.objects.get_or_create(user=self.request.user)
            
        except User.DoesNotExist:
            return Response({"error":"User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        #setting streak
        current_date = timezone.localtime(timezone.now()).date()
        last_updated_date = smile.streak_date
        
        if last_updated_date is None:
            last_updated_date = current_date

        # Calculate the number of days passed
        days_passed = (current_date - last_updated_date).days

        print(last_updated_date)
        print(current_date)
        print(days_passed)
        # Check if the user accessed the app today
        if (current_date - last_updated_date).days == 1:
            
            # updating streak
            smile.streak += 1
            if smile.max_streak < smile.streak:
                smile.max_streak = smile.streak
                
            smile.streak_date = current_date

            

            # updating smile avg
            smile.smile_avg = (smile.smile_avg + smile.smile_sec) / 2

            # reseting goal
            goal.smile_count = 0
            goal.smile_sec = 0
            
            goal = goal_setter(goal)
            # reset smile sec & smile Count
            smile.smile_sec = 0
            smile.smile_count = 0
            
            
            goal.save()
            level.save()
            smile.save()
        # if user accessed after 2 or more days
        elif (current_date - last_updated_date).days > 1:
            smile.streak = 0
            smile.streak_date = current_date
            
            # reseting goal
            goal.smile_count = 0
            goal.smile_sec = 0
            goal = goal_setter(goal)

            # reset smile sec & smile Count
            smile.smile_sec = 0
            smile.smile_count = 0

            # goal.save()
            level.save()
            smile.save()
        else:
            try:
                goal = goal_setter(goal)
                goal.save()
            except:
                pass

        goal = Goal.objects.get(user=self.request.user)
        goal_serializer = GoalSerializer(goal)
        smile_serializer = SmileSerializer(smile)
        response_data = {
            'user':user_serializer.data,
            'smile':smile_serializer.data,
            'goal':goal_serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def patch(self, request):
        smile = Smile.objects.get(user=self.request.user)
        level = Level.objects.get(user=self.request.user)
        
        serializer = SmileSerializer(instance=smile ,data = request.data, partial=True)

        if serializer.is_valid():
            smile_sec = serializer.validated_data['smile_sec'] # lets say = 180 input

            # client side will calculate smile count with smile count = smile sec // 10
            smile_count = serializer.validated_data['smile_count'] # then smile count = 18 input

            if smile_sec > smile.best_smile:
                serializer.validated_data['best_smile'] = smile_sec
            else:
                serializer.validated_data['best_smile'] = smile.best_smile
            
            
            old_smile_count = smile.smile_count
            if smile_count > old_smile_count:
                level.points = smile_count - old_smile_count
            
                # setting level
                level.total_points +=level.points
                required_points = 100*(level.current_level + 1)**2
                if level.total_points >= required_points:
                    level.total_points -= required_points
                    level.current_level += 1

            level.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class GoalView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get(self, request):
        smile = Smile.objects.get(user=self.request.user)
        level = Level.objects.get(user=self.request.user)
        goal = Goal.objects.get(user=self.request.user)
        
        smile_serializer = SmileSerializer(smile)
        level_serializer = LevelSerializer(level)
        goal_serializer = GoalSerializer(goal)
        
        response_data = {
            'goal':goal_serializer.data,
            'level': level_serializer.data,
            'smile': smile_serializer.data,
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


class StatsView(APIView):
    def get(self, request):
        smile = Smile.objects.get(user=self.request.user)
        
        serializer = SmileSerializer(smile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LevelView(APIView):
    def get(self, request):
        level = Level.objects.get(user=self.request.user)
        serializer = LevelSerializer(level)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ActivityView(generics.ListAPIView):
    queryset = Activity.objects.all().order_by('-created_at')[:4]
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = ActivitySerializer


class ActivityDetialView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def post(self, request, pk):
        try:
            activity = Activity.objects.get(id=pk)
            serializer = ActivitySerializer(activity)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'error':"invalid ID"}, status=status.HTTP_400_BAD_REQUEST)


class ImageView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateComunityView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def post(self,request):
        serializer = CommunitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(admin = self.request.user, current_users=1)
            community = Community.objects.get(admin=self.request.user)

            # add current user to community he just created cuz he's a member too
            join_self = UserJoinedCommunity.objects.create(
                user = self.request.user,
                community = community,
                joined = True,
            )
            join_self.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JoinCommunityView(APIView):
    def post(self, reqeust, pk):
        user = self.request.user
        community = Community.objects.get(id=pk)
        
        if UserJoinedCommunity.objects.filter(user=user, community=community).exists():
            return Response({'error': 'Already a member!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            community.current_users += 1
            community.save()
        except:
            return Response({"error":"community full"}, status=status.HTTP_403_FORBIDDEN)
        # If not, create a new UserJoinedCommunity entry
        join_com = UserJoinedCommunity.objects.create(
            user=user,
            community=community,
            joined=True,
        )
        join_com.save()

        return Response({'success': 'Joined the community!'}, status=status.HTTP_201_CREATED)


class CreatePostView(APIView):
    def post(self, request, pk):
        try:
            community = Community.objects.get(id=pk)
        except:
            return Response({"error":"community not Found"}, status=status.HTTP_404_NOT_FOUND)

        joined = UserJoinedCommunity.objects.get(user=self.request.user , community=community)
        if joined is not None:
            serializer = CommPostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user = self.request.user, community=community)
                
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error":"You are not joined in this community"}, status=status.HTTP_403_FORBIDDEN)
        
        
class CreateFriendView(APIView):
    def post(self, request, pk):
        current_user = self.request.user
        
        friend = get_object_or_404(User, id=pk)
        try:
            new_friend = Friend.objects.create(user=current_user, friend=friend)
            serializer = FriendSerializer(data=new_friend)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status==status.HTTP_201_CREATED)
        except:
            return Response({"error":"Already friends"}, status=status.HTTP_400_BAD_REQUEST)