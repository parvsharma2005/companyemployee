from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import (
    EmployeeLeaveBalanceViewSet,
    LeaveRequestViewSet
)

from .views import (
    ManagerLeaveRequestListView,
    LeaveRequestApproveView,
    LeaveRequestRejectView
)

urlpatterns = [

    path(
        "manager/leave-requests/",
        ManagerLeaveRequestListView.as_view(),
        name="manager-leave-requests"
    ),

    path(
        "leave-requests/<uuid:pk>/approve/",
        LeaveRequestApproveView.as_view(),
        name="leave-request-approve"
    ),

    path(
        "leave-requests/<uuid:pk>/reject/",
        LeaveRequestRejectView.as_view(),
        name="leave-request-reject"
    ),
]


router = DefaultRouter()


router.register(
    r"leave-balances",
    EmployeeLeaveBalanceViewSet,
    basename="leave-balance"
)

router.register(
    r"leave-requests",
    LeaveRequestViewSet,
    basename="leave-request"
)

urlpatterns = router.urls