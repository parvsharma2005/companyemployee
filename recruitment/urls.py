from rest_framework.routers import DefaultRouter

from .views import JobOpeningViewSet


router = DefaultRouter()

router.register(
    r"job-openings",
    JobOpeningViewSet,
    basename="job-opening"
)

urlpatterns = router.urls