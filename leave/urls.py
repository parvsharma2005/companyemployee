from rest_framework.routers import DefaultRouter

from .views import (
    LeaveTypeViewSet,
    EmployeeLeaveBalanceViewSet,
    LeaveRequestViewSet
)


router = DefaultRouter()

router.register(
    r"leave-types",
    LeaveTypeViewSet,
    basename="leave-type"
)

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