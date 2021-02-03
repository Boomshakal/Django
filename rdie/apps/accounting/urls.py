from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('retrieve_category/', views.retrieve_category, name='retrieve_category'),
    path('record_income_expense/', views.record_income_expense, name='record_income_expense'),
]
