from rest_framework import serializers
from .models import Movie  # ✅ Change import

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie  # ✅ Change model name
        fields = '__all__'
