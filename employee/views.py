import csv
import io

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Employee
from .serializers import *


class EmployeeListCreateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        department_id = request.query_params.get("department")
        company_id = request.query_params.get("company")

        employees = Employee.objects.all()

        if department_id:
            employees = employees.filter(
                department_id=department_id
            )

        if company_id:
            employees = employees.filter(
                department__company_id=company_id
            )

        serializer = EmployeeSerializer(
            employees,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        serializer = EmployeeSerializer(
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


class EmployeeDetailUpdateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):

        try:
            employee = Employee.objects.get(id=id)

        except Employee.DoesNotExist:
            return Response(
                {"message": "Employee not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EmployeeSerializer(employee)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, id):

        try:
            employee = Employee.objects.get(id=id)

        except Employee.DoesNotExist:
            return Response(
                {"message": "Employee not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EmployeeSerializer(
            employee,
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
            employee = Employee.objects.get(id=id)

        except Employee.DoesNotExist:
            return Response(
                {"message": "Employee not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        employee.delete()

        return Response(
            {"message": "Employee deleted successfully"},
            status=status.HTTP_200_OK
        )


class EmployeeBulkUploadView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        # Get uploaded file
        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "File is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check CSV file
        if not file.name.endswith(".csv"):
            return Response(
                {"error": "Only CSV files are allowed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Read CSV file
            decoded_file = file.read().decode("utf-8")

            csv_data = csv.DictReader(
                io.StringIO(decoded_file)
            )

        except Exception as e:
            return Response(
                {
                    "error": "Unable to read CSV file",
                    "details": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        created_employees = []
        errors = []

        # Process each row
        for row_number, row in enumerate(csv_data, start=2):

            serializer = EmployeeSerializer(
                data=row
            )

            if serializer.is_valid():
                employee = serializer.save()

                created_employees.append(
                    serializer.data
                )

            else:
                errors.append(
                    {
                        "row": row_number,
                        "errors": serializer.errors
                    }
                )

        return Response(
            {
                "message": "Bulk upload completed",
                "created_count": len(created_employees),
                "error_count": len(errors),
                "created": created_employees,
                "errors": errors
            },
            status=status.HTTP_201_CREATED
        )
        
class EmployeeBulkCreateView(APIView):

    def post(self, request):

        serializer = EmployeeBulkSerializer(
            data=request.data,
            many=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Employees created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )