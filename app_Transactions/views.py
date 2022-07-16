from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Transaction
from .forms import TransactionCreateForm


class TransactionCreateListView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionCreateForm
    success_url = reverse_lazy("Transaction:listtransactions")
    template_name = "panel/transactions.html"

    def form_valid(self, form):
        transaction = form.save(commit=False)
        transaction.user = self.request.user
        transaction.reference_id = transaction.id
        return super(TransactionCreateListView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TransactionCreateListView, self).get_context_data(**kwargs)
        context['transaction_list'] = Transaction.objects.filter(user=self.request.user)
        return context
