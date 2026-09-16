from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import *

from .models import Company
from .serializers import companySerializer


class companyListCreateView(APIView):

    def get(self, request):
        companies = Company.objects.all()
        serializer = companySerializer(companies, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

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
            status=status.HTTP_400_BAD_REQUEST
        )


class companyDetailUpdateView(APIView):

    def get(self, request, id):
        try:
            company = Company.objects.get(id=id)

        except Company.DoesNotExist:
            return Response(
                {"message": "company not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = companySerializer(company)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, id):
        try:
            company = Company.objects.get(id=id)

        except Company.DoesNotExist:
            return Response(
                {"message": "company not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = companySerializer(
            company,
            data=request.data
        )

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
            company = Company.objects.get(id=id)

        except Company.DoesNotExist:
            return Response(
                {"message": "company not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        company.delete()

        return Response(
            {"message": "company deleted successfully"},
            status=status.HTTP_200_OK
        )