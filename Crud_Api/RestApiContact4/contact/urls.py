from django.urls import path
from .views import ContactListCreateAPIView, ContactRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('contacts/', ContactListCreateAPIView.as_view(), name='api_contact_list'),
    path('contacts/<int:pk>/', ContactRetrieveUpdateDestroyAPIView.as_view(), name='api_contact_detail'),
]  # ✅ Add closing bracket if missing
