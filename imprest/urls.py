from rest_framework.routers import DefaultRouter

from .views import ImprestRequestViewSet


router = DefaultRouter()

router.register(
    r"imprest",
    ImprestRequestViewSet,
    basename="imprest"
)

urlpatterns = router.urls