from django.urls import path
from .views import *


urlpatterns = [

    path(
        "employees/",
        EmployeeListCreateView.as_view(),
        name="employee-list-create"
    ),

    path(
        "employees/bulk-upload/",
        EmployeeBulkUploadView.as_view(),
        name="employee-bulk-upload"
    ),

    path(
        "employees/<uuid:id>/",
        EmployeeDetailUpdateView.as_view(),
        name="employee-detail-update"
    ),
    path(
        "bulk-create/",
        EmployeeBulkCreateView.as_view()
    ),
    
]