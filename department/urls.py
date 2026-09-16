from django.urls import path
from .views import (
    DepartmentListCreateView,
    DepartmentDetailView
)

urlpatterns = [
    path(
        "department/",
        DepartmentListCreateView.as_view(),
        name="department-list-create"
    ),

    path(
        "department/<uuid:pk>/",
        DepartmentDetailView.as_view(),
        name="department-detail"
    ),
]