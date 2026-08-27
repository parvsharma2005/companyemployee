from rest_framework.routers import DefaultRouter

from .views import EmployeeHistoryLogViewSet


router = DefaultRouter()

router.register(
    r"history",
    EmployeeHistoryLogViewSet,
    basename="employee-history"
)

urlpatterns = router.urls