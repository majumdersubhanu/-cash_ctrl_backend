from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'payment_type', 'transaction_type', 'amount', 'date')
    list_filter = ('payment_type', 'transaction_type', 'date')
    search_fields = ('name', 'user__username', 'user__email')
    readonly_fields = ('date',)  # If you have auto_now_add=True on the date field

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set user during the first save.
            obj.user = request.user
        super().save_model(request, obj, form, change)
