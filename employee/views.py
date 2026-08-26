import csv
import io

from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.pagination import PageNumberPagination

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Employee, EmployeeAccount

from .serializers import (
    EmployeeSerializer,
    EmployeeBulkSerializer,
    LoginSerializer
)


# =========================================================
# Employee List + Create
# =========================================================

class EmployeeListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    # =====================================================
    # GET ALL EMPLOYEES
    # =====================================================

    def get(self, request):

        employees = Employee.objects.all()

        # -------------------------------------------------
        # Ordering
        # -------------------------------------------------

        ordering = request.query_params.get(
            "ordering"
        )

        if ordering:

            employees = employees.order_by(
                ordering
            )

        # -------------------------------------------------
        # Serializer
        # -------------------------------------------------

        serializer = EmployeeSerializer(
            employees,
            many=True,
            context={
                "request": request
            }
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # =====================================================
    # CREATE EMPLOYEE
    # =====================================================

    def post(self, request):

        serializer = EmployeeSerializer(
            data=request.data,
            context={
                "request": request
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        employee = serializer.save()

        response_serializer = EmployeeSerializer(
            employee,
            context={
                "request": request
            }
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


# =========================================================
# Employee Detail / Update / Delete
# =========================================================

class EmployeeDetailUpdateView(APIView):

    permission_classes = [IsAuthenticated]

    # =====================================================
    # GET EMPLOYEE
    # =====================================================

    def get(self, request, id):

        try:

            employee = Employee.objects.get(
                id=id
            )

        except Employee.DoesNotExist:

            return Response(
                {
                    "message":
                    "Employee not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EmployeeSerializer(
            employee,
            context={
                "request": request
            }
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # =====================================================
    # UPDATE EMPLOYEE
    # =====================================================

    def put(self, request, id):

        try:

            employee = Employee.objects.get(
                id=id
            )

        except Employee.DoesNotExist:

            return Response(
                {
                    "message":
                    "Employee not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EmployeeSerializer(
            employee,
            data=request.data,
            partial=True,
            context={
                "request": request
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        employee = serializer.save()

        response_serializer = EmployeeSerializer(
            employee,
            context={
                "request": request
            }
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK
        )

    # =====================================================
    # DELETE EMPLOYEE
    # =====================================================

    def delete(self, request, id):

        try:

            employee = Employee.objects.get(
                id=id
            )

        except Employee.DoesNotExist:

            return Response(
                {
                    "message":
                    "Employee not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        employee.delete()

        return Response(
            {
                "message":
                "Employee deleted successfully."
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# CSV Bulk Upload
# =========================================================

class EmployeeBulkUploadView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        file = request.FILES.get(
            "file"
        )

        # -------------------------------------------------
        # Check file
        # -------------------------------------------------

        if not file:

            return Response(
                {
                    "error":
                    "File is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -------------------------------------------------
        # Check CSV
        # -------------------------------------------------

        if not file.name.lower().endswith(
            ".csv"
        ):

            return Response(
                {
                    "error":
                    "Only CSV files are allowed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -------------------------------------------------
        # Read CSV
        # -------------------------------------------------

        try:

            decoded_file = file.read().decode(
                "utf-8-sig"
            )

            csv_data = csv.DictReader(
                io.StringIO(decoded_file)
            )

        except Exception as e:

            return Response(
                {
                    "error":
                    "Unable to read CSV file.",
                    "details":
                    str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        created_employees = []
        errors = []

        # -------------------------------------------------
        # Process rows
        # -------------------------------------------------

        for row_number, row in enumerate(
            csv_data,
            start=2
        ):

            serializer = EmployeeSerializer(
                data=row,
                context={
                    "request": request
                }
            )

            if serializer.is_valid():

                try:

                    employee = serializer.save()

                    response_serializer = (
                        EmployeeSerializer(
                            employee,
                            context={
                                "request": request
                            }
                        )
                    )

                    created_employees.append(
                        response_serializer.data
                    )

                except Exception as e:

                    errors.append(
                        {
                            "row":
                            row_number,
                            "errors":
                            str(e)
                        }
                    )

            else:

                errors.append(
                    {
                        "row":
                        row_number,
                        "errors":
                        serializer.errors
                    }
                )

        # -------------------------------------------------
        # Response
        # -------------------------------------------------

        return Response(
            {
                "message":
                "Bulk upload completed.",
                "created_count":
                len(created_employees),
                "error_count":
                len(errors),
                "created":
                created_employees,
                "errors":
                errors
            },
            status=status.HTTP_201_CREATED
        )


# =========================================================
# JSON Bulk Create
# =========================================================

class EmployeeBulkCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = EmployeeBulkSerializer(
            data=request.data,
            many=True,
            context={
                "request": request
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        employees = serializer.save()

        response_serializer = EmployeeSerializer(
            employees,
            many=True,
            context={
                "request": request
            }
        )

        return Response(
            {
                "message":
                "Employees created successfully.",
                "data":
                response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )


# =========================================================
# Employee Search
# =========================================================

class EmployeeSearchView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        search = request.query_params.get(
            "search"
        )

        # -------------------------------------------------
        # Search required
        # -------------------------------------------------

        if not search:

            return Response(
                {
                    "message":
                    "Please provide employee name."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -------------------------------------------------
        # Search employee
        # -------------------------------------------------

        employees = Employee.objects.filter(
            name__iexact=search
        )

        if not employees.exists():

            return Response(
                {
                    "message":
                    "Employee not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # -------------------------------------------------
        # Ordering
        # -------------------------------------------------

        ordering = request.query_params.get(
            "ordering"
        )

        if ordering:

            employees = employees.order_by(
                ordering
            )

        # -------------------------------------------------
        # Pagination
        # -------------------------------------------------

        paginator = PageNumberPagination()

        paginator.page_size = 10

        paginated_employees = (
            paginator.paginate_queryset(
                employees,
                request
            )
        )

        # -------------------------------------------------
        # Serializer
        # -------------------------------------------------

        serializer = EmployeeSerializer(
            paginated_employees,
            many=True,
            context={
                "request": request
            }
        )

        return paginator.get_paginated_response(
            serializer.data
        )


# =========================================================
# Login
# =========================================================

class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        account = serializer.validated_data[
            "account"
        ]

        # -------------------------------------------------
        # Create JWT
        # -------------------------------------------------

        refresh = RefreshToken.for_user(
            account
        )

        return Response(
            {
                "message":
                "Login successful.",

                "refresh":
                str(refresh),

                "access":
                str(
                    refresh.access_token
                )
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# Employee Account Registration
# =========================================================

class EmployeeRegisterView(APIView):

    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):

        phone = request.data.get(
            "phone"
        )

        email = request.data.get(
            "email"
        )

        password = request.data.get(
            "password"
        )

        # =================================================
        # REQUIRED FIELDS
        # =================================================

        if not phone:

            return Response(
                {
                    "phone":
                    "Phone number is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not email:

            return Response(
                {
                    "email":
                    "Email is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not password:

            return Response(
                {
                    "password":
                    "Password is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # =================================================
        # PHONE VALIDATION
        # =================================================

        if not phone.isdigit():

            return Response(
                {
                    "phone":
                    "Phone number must contain numbers only."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(phone) != 10:

            return Response(
                {
                    "phone":
                    "Phone number must contain exactly 10 digits."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # =================================================
        # PASSWORD VALIDATION
        # =================================================

        if len(password) < 8:

            return Response(
                {
                    "password":
                    "Password must be at least 8 characters."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # =================================================
        # DUPLICATE PHONE
        # =================================================

        if EmployeeAccount.objects.filter(
            phone=phone
        ).exists():

            return Response(
                {
                    "phone":
                    "This phone number is already registered."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # =================================================
        # DUPLICATE EMAIL
        # =================================================

        if EmployeeAccount.objects.filter(
            email=email
        ).exists():

            return Response(
                {
                    "email":
                    "An account with this email already exists."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # =================================================
        # CREATE ACCOUNT
        # =================================================

        account = EmployeeAccount(
            phone=phone,
            email=email
        )

        # -------------------------------------------------
        # Hash password
        # -------------------------------------------------

        account.set_password(
            password
        )

        # -------------------------------------------------
        # Save
        # -------------------------------------------------

        account.save()

        # =================================================
        # RESPONSE
        # =================================================

        return Response(
            {
                "message":
                "User registered successfully.",
                "phone":
                account.phone,
                "user_id": str(account.id),
                "email":
                account.email
            },
            status=status.HTTP_201_CREATED
        )


# =========================================================
# Forgot Password
# =========================================================

class ForgotPasswordView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        phone = request.data.get(
            "phone"
        )

        # -------------------------------------------------
        # Check phone
        # -------------------------------------------------

        if not phone:

            return Response(
                {
                    "phone":
                    "Phone number is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -------------------------------------------------
        # Find account
        # -------------------------------------------------

        try:

            account = EmployeeAccount.objects.get(
                phone=phone
            )

        except EmployeeAccount.DoesNotExist:

            return Response(
                {
                    "message":
                    "No account found with this phone number."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # -------------------------------------------------
        # Development response
        # -------------------------------------------------

        return Response(
            {
                "message":
                "Account found. OTP verification is required."
            },
            status=status.HTTP_200_OK
        )