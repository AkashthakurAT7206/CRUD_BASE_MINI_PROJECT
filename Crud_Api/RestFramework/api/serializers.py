
from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        # fields = ( ) or []
        fields = '__all__'
        read_only_fields = ('created_at','updated_at')
