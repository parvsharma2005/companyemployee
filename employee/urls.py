from django.urls import path
from .views import *


urlpatterns = [
    
    path(
        "register/",
        EmployeeRegisterView.as_view(),
        name="employee-register"
    ),
    
    path(
    "forgot-password/",
    ForgotPasswordView.as_view(),
    name="forgot-password"
),
    
    path(
    "login/",
    LoginView.as_view(),
    name="login"
    ),

    path(
        "employees/",
        EmployeeListCreateView.as_view(),
        name="employee-list-create"
    ),
    
    
]
    
path(
    "employees/search/",
    EmployeeSearchView.as_view(),
    name="employee-search"
),

path(
        "employees/bulk-upload/",
        EmployeeBulkUploadView.as_view(),
        name="employee-bulk-upload"
    ),

path(
        "bulk-create/",
        EmployeeBulkCreateView.as_view()
    ),

path(
        "employees/<uuid:id>/",
        EmployeeDetailUpdateView.as_view(),
        name="employee-detail-update"
    ),


