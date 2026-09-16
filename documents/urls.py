from rest_framework.routers import DefaultRouter

from .views import EmployeeDocumentViewSet


router = DefaultRouter()

router.register(
    r"documents",
    EmployeeDocumentViewSet,
    basename="employee-document"
)

urlpatterns = router.urls