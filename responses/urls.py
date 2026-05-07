from django.urls import path
from . import views

urlpatterns = [
    path('my/', views.MyResponsesView.as_view(), name='my_responses'),
    path('create/<int:ad_pk>/', views.ResponseCreateView.as_view(), name='response_create'),
    path('accept/<int:pk>/', views.accept_response, name='accept_response'),
    path('delete/<int:pk>/', views.delete_response, name='delete_response'),
]