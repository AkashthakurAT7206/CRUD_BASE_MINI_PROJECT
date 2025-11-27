
from django.urls import path
from .views import EmployeeListCreate, EmployeeDetail

urlpatterns = [
    path('employees/', EmployeeListCreate.as_view()),
    path('employees/<int:pk>/', EmployeeDetail.as_view()),
]
