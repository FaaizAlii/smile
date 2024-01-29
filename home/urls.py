from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.DashBoardView.as_view(), name='dashboard'),
    path('goals/', views.GoalView.as_view(), name='goals'),
    path('stats/', views.StatsView.as_view(), name='stats'),
    path('level/', views.LevelView.as_view(), name='level'),
    path('activites/', views.ActivityView.as_view(), name='activites'),
    path('activity-detail/<int:pk>/', views.ActivityDetialView.as_view(), name='activity-detail'),
    path('upload-image/', views.ImageView.as_view(), name='upload-image'),
    path('create-community/', views.CreateComunityView.as_view(), name='create-community'),
    path('join-community/<int:pk>/', views.JoinCommunityView.as_view(), name='join-community'),
    path('create-community-post/<int:pk>/', views.CreatePostView.as_view(), name='create-community-post'),
]