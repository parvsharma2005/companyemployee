from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Department
from .serializers import DepartmentSerializer


# =========================================================
# Department List + Create
# =========================================================

class DepartmentListCreateView(APIView):

    # GET - Get all departments
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

    # POST - Create a new department
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


# =========================================================
# Department Detail + Update + Delete
# =========================================================

class DepartmentDetailView(APIView):

    # Get department object by UUID
    def get_object(self, pk):

        try:
            return Department.objects.get(pk=pk)

        except Department.DoesNotExist:
            return None

    # GET - Get one department
    def get(self, request, pk):

        department = self.get_object(pk)

        if department is None:

            return Response(
                {
                    "message": "Department not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = DepartmentSerializer(
            department
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # PUT - Update complete department
    def put(self, request, pk):

        department = self.get_object(pk)

        if department is None:

            return Response(
                {
                    "message": "Department not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = DepartmentSerializer(
            department,
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

    # PATCH - Update partial department
    def patch(self, request, pk):

        department = self.get_object(pk)

        if department is None:

            return Response(
                {
                    "message": "Department not found"
                },
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

    # DELETE - Delete department
    def delete(self, request, pk):

        department = self.get_object(pk)

        if department is None:

            return Response(
                {
                    "message": "Department not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        department.delete()

        return Response(
            {
                "message": "Department deleted successfully"
            },
            status=status.HTTP_200_OK
        )
