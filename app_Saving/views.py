from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Saving, SavingPaymentLog
from .forms import SavingCreateForm, SavingPaymentCreateForm


class SavingListCreateView(LoginRequiredMixin, CreateView):
    model = Saving
    form_class = SavingCreateForm
    success_url = reverse_lazy("Saving:listsaving")
    template_name = "panel/saving.html"

    def form_valid(self, form):
        saving_object = form.save(commit=False)
        saving_object.user = self.request.user
        return super(SavingListCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SavingListCreateView, self).get_context_data(**kwargs)
        context['saving_list'] = Saving.objects.filter(user=self.request.user)
        return context


class SavingDeleteView(LoginRequiredMixin, DeleteView):
    model = Saving
    success_url = reverse_lazy("Saving:listsaving")

    def get_queryset(self):
        return Saving.objects.filter(user=self.request.user)

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class PaymentSavingView(LoginRequiredMixin, CreateView):
    model = SavingPaymentLog
    form_class = SavingPaymentCreateForm
    success_url = reverse_lazy("Saving:listsaving")

    def form_valid(self, form):
        saving_object = Saving.objects.filter(user=self.request.user, pk=self.kwargs['pk']).first()
        if saving_object:
            saving_payment_object = form.save(commit=False)
            saving_payment_object.saving = saving_object
        return super(PaymentSavingView, self).form_valid(form)
