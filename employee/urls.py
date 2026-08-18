from django.urls import path
from .views import *


urlpatterns = [
    path(
        '',
        EmployeeListCreateView.as_view(),
        name='employee-list-create'
    ),

    path(
        'employees/<str:id>/',
        EmployeeDetailUpdateView.as_view(),
        name='employee-detail'
    ),
]