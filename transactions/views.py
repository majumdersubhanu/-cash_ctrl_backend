from rest_framework import permissions, viewsets
from .models import Transaction
from .serializers import TransactionSerializer
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if not user.is_superuser:
            queryset = queryset.filter(user=user)

        payment_type = self.request.query_params.get('payment_type', None)
        transaction_type = self.request.query_params.get('transaction_type', None)

        if payment_type:
            queryset = queryset.filter(payment_type=payment_type)
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def total_expenditure_current_month(self, request):
        month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        total = self.get_queryset().filter(
            transaction_type='expense',
            date__gte=month_start
        ).aggregate(Sum('amount'))
        return Response({'total_expenditure_current_month': total['amount__sum']})

    @action(detail=False, methods=['get'])
    def category_wise_expenses(self, request):
        queryset = self.get_queryset().filter(transaction_type='expense')

        category_param = self.request.query_params.get('category', None)
        if category_param:
            queryset = queryset.filter(category=category_param)

        category_expenses = queryset.values('category').annotate(total_amount=Sum('amount')).order_by('category')

        response_data = {item['category']: item['total_amount'] for item in category_expenses}
        return Response(response_data)

    @action(detail=False, methods=['get'])
    def total_expenditure_current_year(self, request):
        year_start = timezone.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        total = self.get_queryset().filter(
            transaction_type='expense',
            date__gte=year_start
        ).aggregate(Sum('amount'))
        return Response({'total_expenditure_current_year': total['amount__sum']})

    @action(detail=False, methods=['get'])
    def total_expenditure_all_time(self, request):
        total = self.get_queryset().filter(
            transaction_type='expense'
        ).aggregate(Sum('amount'))
        return Response({'total_expenditure_all_time': total['amount__sum']})

    @action(detail=False, methods=['get'])
    def total_income_current_month(self, request):
        month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        total = self.get_queryset().filter(
            transaction_type='income',
            date__gte=month_start
        ).aggregate(Sum('amount'))
        return Response({'total_income_current_month': total['amount__sum']})

    @action(detail=False, methods=['get'])
    def month_wise_expenses(self, request):
        current_year = timezone.now().year
        month_wise_expenses = self.get_queryset().filter(
            transaction_type='expense',
            date__year=current_year
        ).annotate(month=TruncMonth('date')).values('month').annotate(total_amount=Sum('amount')).order_by('month')
        return Response([item['total_amount'] for item in month_wise_expenses])
