

from django.urls import path , include

from rest_framework.routers import DefaultRouter
from .views import TodoViewSet

router = DefaultRouter()

router.register(r'todos',TodoViewSet,basename='todo')
# After registration, the router automatically creates these URLs:
# - GET /todos/ - List all todos (TodoViewSet.list)
# - POST /todos/ - Create a new todo (TodoViewSet.create)
# - GET /todos/{id}/ - Retrieve a specific todo (TodoViewSet.retrieve)
# - PUT /todos/{id}/ - Update a todo completely (TodoViewSet.update)
# - PATCH /todos/{id}/ - Partially update a todo (TodoViewSet.partial_update)
# - DELETE /todos/{id}/ - Delete a todo (TodoViewSet.destroy)

urlpatterns = [
    path('',include(router.urls)),
   
]
