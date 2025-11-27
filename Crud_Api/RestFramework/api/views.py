from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets , status
from rest_framework.response import Response

from rest_framework.decorators import action

from .models import Todo
from .serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    """
    viewset for todo curd operations
    list :getall todos
    create 
    retrieve  
    update
    partial update
    destroy or delete
    """
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    def get_queryset(self):
        queryset = Todo.objects.all()
        completed  = self.request.query_params.get('completed',None)
        
        if completed is not None:
            completed_bool = completed.lower() =='true'
            queryset =queryset.filter(completed=completed_bool)
        return queryset
    
    # @action(detail=False,methods=['get'])
    # def completed(self,request):
    #     completed_todos = self.get_queryset().filter(completed=True)
    #     serializer = self.get_serializer(completed_todos,many=True)
    #     return Response(serializer.data)
    
    # @action(detail=False,methods=['get'])
    # def pending(self,request):
    #     pending_todos = self.get_queryset().filter(completed=False)
    #     serializer = self.get_serializer(pending_todos,many=True)
    #     return Response(serializer.data)