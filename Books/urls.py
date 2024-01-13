from django.shortcuts import render

from django.urls import path
from .import views


urlpatterns = [
    path('details/<int:id>',views.detail,name='details'),
    path('buy/<int:id>',views.buy,name='buynow'),
    path('return/<int:id>',views.returning,name='return'),
    path('comment/<int:id>',views.comment,name='comment'),

]
