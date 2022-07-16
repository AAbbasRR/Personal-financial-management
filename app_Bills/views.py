from django.views.generic import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Bill
from .forms import BillCreateForm


class BillCreateListView(LoginRequiredMixin, CreateView):
    model = Bill
    form_class = BillCreateForm
    success_url = reverse_lazy("Bill:listbills")
    template_name = "panel/bills.html"

    def form_valid(self, form):
        bill_object = form.save(commit=False)
        bill_object.user = self.request.user
        return super(BillCreateListView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(BillCreateListView, self).get_context_data(**kwargs)
        context['bills_list'] = Bill.objects.filter(user=self.request.user)
        return context


class BillDeleteView(LoginRequiredMixin, DeleteView):
    model = Bill
    success_url = reverse_lazy("Bill:listbills")

    def get_queryset(self):
        return Bill.objects.filter(user=self.request.user)

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
