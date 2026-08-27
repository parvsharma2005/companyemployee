from rest_framework.routers import DefaultRouter

from .views import InvestmentDeclarationViewSet


router = DefaultRouter()

router.register(
    r"investments",
    InvestmentDeclarationViewSet,
    basename="investment"
)

urlpatterns = router.urls