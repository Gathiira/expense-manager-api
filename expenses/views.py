import datetime

from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.pagination import PageNumberPagination

from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils import timezone

from drf_yasg.utils import swagger_auto_schema

from util.permissions import IsOwner

from .serializers import ExpenseSerializer, IncomeSerializer
from .models import ExpenseModel, IncomeModel


@permission_classes([IsOwner])
class ExpenseView(viewsets.ModelViewSet):
	queryset = ExpenseModel.objects.order_by('-created_at')
	pagination_class = PageNumberPagination

	lookup_field = 'id'

	@swagger_auto_schema(request_body=ExpenseSerializer)
	@action(methods=['POST'], detail=False, url_path='add-expense', url_name='add_expense')
	def add_expense(self, request):
		data = request.data
		data['owner'] = request.user.id

		serializer = ExpenseSerializer(data=data, many=False)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data, status=status.HTTP_201_CREATED)

	@action(methods=['GET'], detail=False, url_path='list-expenses', url_name='list_expenses')
	def list_expenses(self, request):
		data = get_list_or_404(self.queryset,owner=request.user)
		serializer = ExpenseSerializer(data, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@action(methods=['DELETE'], detail=False, url_path='delete-expense', url_name='delete_expense')
	def delete_expense(self,request):
		expense_id = request.query_params.get('expenseID')
		expense = get_object_or_404(self.queryset, owner=request.user, id=expense_id)
		expense.delete()
		return Response({'detail': 'Item deleted'}, status=status.HTTP_204_NO_CONTENT)

	def get_category(self, expense):
		return expense.category

	def get_amount_for_category(self, expense_list, category):
		expenses = expense_list.filter(category=category)
		amount = 0

		for expense in expenses:
			amount += expense.amount

		return {'amount':str(amount)}

	@action(methods=['GET'], detail=False, url_path='expense-stats', url_name='expense_stats')
	def get_stats(self, request):
		todays_date = datetime.datetime.now(tz=timezone.utc)
		a_year_ago = todays_date - datetime.timedelta(days=30*12)

		expenses = ExpenseModel.objects.filter(
			owner=request.user, created_at__gte=a_year_ago, created_at__lte=todays_date)
		categories = list(set(map(self.get_category, expenses)))

		final = {}
		for expense in expenses:
			for category in categories:
				final[category] = self.get_amount_for_category(expenses, category)

		return Response({'category_data':final}, status=status.HTTP_200_OK)

@permission_classes([IsOwner])
class IncomeView(viewsets.ModelViewSet):
	queryset = IncomeModel.objects.order_by('-created_at')
	
	@action(methods=['POST'], detail=False, url_path='add-income', url_name='add_income')
	def add_income(self, request):
		data = request.data

		data['owner'] = request.user.id

		serializer = IncomeSerializer(data=data, many=False)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data, status=status.HTTP_201_CREATED)

	@action(methods=['GET'], detail=False, url_path='my-income', url_name='my_income')
	def list_income(self, request):
		income = get_list_or_404(self.queryset, owner=request.user)
		serializer = IncomeSerializer(income, many=True)
		return Response(serializer.data)
	
	@action(methods=['DELETE'], detail=True, url_path='delete-income', url_name='delete_income')
	def delete_income(self, request, pk=None):
		# income_id = request.query_params.get('incomeID')
		income = get_object_or_404(self.queryset, owner=request.user, id=pk)
		income.delete()
		return Response({'detail':'Income cleared'}, status=status.HTTP_204_NO_CONTENT)

