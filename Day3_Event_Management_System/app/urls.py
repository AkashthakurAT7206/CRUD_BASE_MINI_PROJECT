from django.urls import path
from .views import (
    EventListView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
)

urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('create/', EventCreateView.as_view(), name='event_create'),
    path('update/<int:pk>/', EventUpdateView.as_view(), name='event_update'),  
    path('delete/<int:pk>/', EventDeleteView.as_view(), name='event_delete'),  

]
