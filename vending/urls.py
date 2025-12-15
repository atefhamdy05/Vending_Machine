from django.urls import path
from .views import  Buy, Reset,Deposit

urlpatterns = [
    path('deposit/', Deposit.as_view()),
    path('buy/', Buy.as_view()),
    path('reset/', Reset.as_view()),
]
