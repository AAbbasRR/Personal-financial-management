from django.views.generic import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Receipt
from .forms import ReceiptCreateForm


class ReceiptCreateListView(LoginRequiredMixin, CreateView):
    model = Receipt
    form_class = ReceiptCreateForm
    success_url = reverse_lazy("Receipt:listreceipt")
    template_name = "panel/receipts.html"

    def form_valid(self, form):
        receipt_object = form.save(commit=False)
        receipt_object.user = self.request.user
        return super(ReceiptCreateListView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ReceiptCreateListView, self).get_context_data(**kwargs)
        context['receipt_list'] = Receipt.objects.filter(user=self.request.user)
        return context


class ReceiptDeleteView(LoginRequiredMixin, DeleteView):
    model = Receipt
    success_url = reverse_lazy("Receipt:listreceipt")

    def get_queryset(self):
        return Receipt.objects.filter(user=self.request.user)

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
