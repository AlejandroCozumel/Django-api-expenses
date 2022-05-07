from django.shortcuts import render
from rest_framework.views import APIView
from expenses.models import Expense
from incomes.models import Income
from rest_framework.response import Response
from rest_framework import status
import datetime
import pdb

# Create your views here.
class ExpenseSummaryStats(APIView):

  def get_amount_for_category(self, expense_list, category):
    expenses = expense_list.filter(category=category)
    ammount = 0

    for expense in expenses:
      ammount += expense.ammount
    return {'amount': str(ammount)}

  def get_category(self, expense):
    return expense.category

  def get(self, request):
    todays_date = datetime.date.today()
    a_year_ago = todays_date - datetime.timedelta(days=365)
    expenses = Expense.objects.filter(owner=request.user, date__gte=a_year_ago, date__lte=todays_date)

    final = {}
    categories = list(set(map(self.get_category, expenses)))


    for category in categories:
        # pdb.set_trace()
      final[category] = self.get_amount_for_category(expenses, category)
        
    return Response({'category_data': final}, status=status.HTTP_200_OK)

class IncomeSourcesSummaryStats(APIView):

  def get_income_source(self, income_list, source):
    income = income_list.filter(source=source)
    ammount = 0

    for i in income:
      ammount += i.ammount
    return {'amount': str(ammount)}

  def get_source(self, income):
    return income.source

  def get(self, request):
    todays_date = datetime.date.today()
    a_year_ago = todays_date - datetime.timedelta(days=365)
    income = Income.objects.filter(owner=request.user, date__gte=a_year_ago, date__lte=todays_date)

    final = {}
    sources = list(set(map(self.get_source, income)))


    for source in sources:
        # pdb.set_trace()
      final[source] = self.get_income_source(income, source)
        
    return Response({'income_source_data': final}, status=status.HTTP_200_OK)
