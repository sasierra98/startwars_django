from rest_framework import views, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from movies.serializers import MovieSerializer
from movies.models import Movie


class MovieView(views.APIView):
    serializer_class = MovieSerializer

    def get(self, request, format=None, *args, **kwargs) -> Response:
        movie = Movie.objects.all()
        serializer = self.serializer_class(movie, many=True)

        return Response(serializer.data)

    def post(self, request, format=None, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieViewDetail(views.APIView):
    serializer_class = MovieSerializer

    @staticmethod
    def get_object(pk: int) -> Movie:
        return get_object_or_404(Movie, id=pk)

    def get(self, request, pk: int, format=None) -> Response:
        movie = self.get_object(pk=pk)
        serializer = self.serializer_class(movie)

        return Response(serializer.data)

    def put(self, request, pk, format=None) -> Response:
        movie = self.get_object(pk)
        serializer = self.serializer_class(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None) -> Response:
        movie = self.get_object(pk)
        serializer = self.serializer_class(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None) -> Response:
        movie = self.get_object(pk)
        movie.delete()
        return Response('Deleted', status=status.HTTP_200_OK)