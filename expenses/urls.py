from rest_framework import routers

from .views import ExpenseView, IncomeView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'expense', ExpenseView, basename= 'expense')
router.register(r'income', IncomeView, basename='income')

urlpatterns = router.urls
