from django.urls import path
from . import views

app_name = 'base'

urlpatterns  =[
    path('list-urls/', views.list_urls.as_view(), name='list-urls'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('profile-step1/', views.Profile1View.as_view(), name='profile1'),
    # path('profile-step2/', views.Profile2View.as_view(), name='profile2'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile-step3/', views.Profile3View.as_view(), name='profile3'),
    path('my_account/', views.MyAccountView.as_view(), name='my_account'),
]