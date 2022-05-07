from .views import ExpenseSummaryStats, IncomeSourcesSummaryStats
from django.urls import path

urlpatterns = [
  path('expense-category-data/', ExpenseSummaryStats.as_view(), name='expense-category-summary'),
  path('income-category-data/', IncomeSourcesSummaryStats.as_view(), name='income-category-summary'),
]