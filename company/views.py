from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *


class companyListCreateView(APIView):

    def get(self, request):
        company = company.objects.all()
        serializer = companySerializer(employees, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = companySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


class companyDetailUpdateView(APIView):

    def get(self, request, id):
        try:
            company = company.objects.get(id=id)
        except company.DoesNotExist:
            return Response(
                {"message": "company not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = companySerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        try:
            company = company.objects.get(id=id)
        except company.DoesNotExist:
            return Response(
                {"message": "company not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = companySerializer(company, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, id):
        try:
            company = company.objects.get(id=id)
        except company.DoesNotExist:
            return Response(
                {"message": "company not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        company.delete()

        return Response(
            {"message": "company deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )