from django.urls import path
from .views import  Buy, Reset,Deposit, transactions_list

urlpatterns = [
    path('deposit/', Deposit.as_view()),
    path('buy/', Buy.as_view()),
    path('reset/', Reset.as_view()),
    path('transactions_list/',transactions_list,name="transaction_list"),

]
