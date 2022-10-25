from drf_yasg.utils import swagger_auto_schema
from rest_framework import views, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from planets.serializers import PlanetSerializer
from planets.models import Planet


class PlanetView(views.APIView):
    serializer_class = PlanetSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs) -> Response:
        planet = Planet.objects.all()
        serializer = self.serializer_class(planet, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializer_class)
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

    @swagger_auto_schema(request_body=serializer_class)
    def put(self, request, pk, format=None) -> Response:
        planet = self.get_object(pk)
        serializer = self.serializer_class(planet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=serializer_class)
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
        return Response(f'Deleted id:{pk}', status=status.HTTP_204_NO_CONTENT)

