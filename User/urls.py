from django.urls import path
from .import views

urlpatterns = [
    path('signup/',views.signup_user.as_view(),name='signup'),
    path('login/',views.login_user.as_view(),name='login'),
    path('profile/',views.profile,name='profile'),
    path('logout/',views.userlogout,name='logout'),
]