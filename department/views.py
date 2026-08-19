from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Department
from .serializers import DepartmentSerializer


class DepartmentListCreateView(APIView):

    def get(self, request):
        departments = Department.objects.all()

        serializer = DepartmentSerializer(
            departments,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        serializer = DepartmentSerializer(
            data=request.data
        )

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


class DepartmentDetailView(APIView):

    def get(self, request, id):

        try:
            department = Department.objects.get(id=id)

        except Department.DoesNotExist:

            return Response(
                {"message": "Department not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = DepartmentSerializer(
            department
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, id):

        try:
            department = Department.objects.get(id=id)

        except Department.DoesNotExist:

            return Response(
                {"message": "Department not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = DepartmentSerializer(
            department,
            data=request.data,
            partial=True
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
            department = Department.objects.get(id=id)

        except Department.DoesNotExist:

            return Response(
                {"message": "Department not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        department.delete()

        return Response(
            {"message": "Department deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
