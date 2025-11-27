from rest_framework import viewsets
from .models import Movie  # ✅ Change import
from .serializers import MovieSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()  # ✅ Change model name
    serializer_class = MovieSerializer
