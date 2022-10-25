from drf_yasg.utils import swagger_auto_schema
from rest_framework import views, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django_filters import rest_framework as filters

from characters.filters import PeopleFilter
from characters.serializers import PeopleSerializer
from characters.models import People


class PeopleView(views.APIView):
    serializer_class = PeopleSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PeopleFilter

    def get(self, request, format=None, *args, **kwargs) -> Response:
        filter_name = self.request.query_params.get('name')
        if filter_name:
            people = People.objects.filter(name=filter_name)
        else:
            people = People.objects.all()
        serializer = self.serializer_class(people, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request, format=None, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PeopleViewDetail(views.APIView):
    serializer_class = PeopleSerializer

    @staticmethod
    def get_object(pk: int) -> People:
        return get_object_or_404(People, id=pk)

    def get(self, request, pk: int, format=None) -> Response:
        people = self.get_object(pk=pk)
        serializer = self.serializer_class(people)

        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializer_class)
    def put(self, request, pk, format=None) -> Response:
        people = self.get_object(pk)
        serializer = self.serializer_class(people, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=serializer_class)
    def patch(self, request, pk, format=None) -> Response:
        people = self.get_object(pk)
        serializer = self.serializer_class(people, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None) -> Response:
        people = self.get_object(pk)
        people.delete()
        return Response(f'Deleted id:{pk}', status=status.HTTP_204_NO_CONTENT)
