from rest_framework.routers import DefaultRouter

from .views import (
    EmployeeLeaveBalanceViewSet,
    LeaveRequestViewSet
)


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