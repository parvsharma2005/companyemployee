from rest_framework.routers import DefaultRouter

from .views import (
    PerformanceReviewViewSet,
    AwardViewSet,
)


router = DefaultRouter()

router.register(
    r"performance-reviews",
    PerformanceReviewViewSet,
    basename="performance-review"
)

router.register(
    r"awards",
    AwardViewSet,
    basename="award"
)

urlpatterns = router.urls