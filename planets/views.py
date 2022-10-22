from rest_framework import views, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from planets.serializers import PlanetSerializer
from planets.models import Planet


class PlanetView(views.APIView):
    serializer_class = PlanetSerializer

    def get(self, request, format=None, *args, **kwargs) -> Response:
        planet = Planet.objects.all()
        serializer = self.serializer_class(planet, many=True)

        return Response(serializer.data)

    def post(self, request, format=None, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlanetViewDetail(views.APIView):
    serializer_class = PlanetSerializer

    @staticmethod
    def get_object(pk: int) -> Planet:
        return get_object_or_404(Planet, id=pk)

    def get(self, request, pk: int, format=None) -> Response:
        planet = self.get_object(pk=pk)
        serializer = self.serializer_class(planet)

        return Response(serializer.data)

    def put(self, request, pk, format=None) -> Response:
        planet = self.get_object(pk)
        serializer = self.serializer_class(planet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None) -> Response:
        planet = self.get_object(pk)
        serializer = self.serializer_class(planet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None) -> Response:
        planet = self.get_object(pk)
        planet.delete()
        return Response('Deleted', status=status.HTTP_200_OK)

