from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from .models import Installments, InstallmentPayments
from .forms import InstallmentsCreateForm


class InstallmentCreateListView(LoginRequiredMixin, CreateView):
    model = Installments
    form_class = InstallmentsCreateForm
    success_url = reverse_lazy("Installments:listinstallments")
    template_name = "panel/installments.html"

    def form_valid(self, form):
        installments = form.save(commit=False)
        installments.user = self.request.user
        return super(InstallmentCreateListView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(InstallmentCreateListView, self).get_context_data(**kwargs)
        context['opened_installments_list'] = Installments.objects.filter(user=self.request.user, status="OPN")
        context['closed_installments_list'] = Installments.objects.filter(user=self.request.user, status="CLS")
        return context


class InstallmentCloseView(LoginRequiredMixin, UpdateView):
    model = Installments

    def get_success_url(self):
        return HttpResponseRedirect(reverse("Installments:listinstallments"))

    def get_queryset(self):
        return Installments.objects.filter(user=self.request.user, status="OPN")

    def get(self, request, *args, **kwargs):
        installment_object = self.get_object()
        if installment_object:
            installment_object.status = "CLS"
            installment_object.save()
            return self.get_success_url()


class InstallmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Installments
    success_url = reverse_lazy("Installments:listinstallments")

    def get_queryset(self):
        return Installments.objects.filter(user=self.request.user, status="CLS")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class PaymentInstallmentView(LoginRequiredMixin, CreateView):
    model = InstallmentPayments
    fields = ['installment']
    success_url = reverse_lazy("Installments:listinstallments")

    def form_valid(self, form):
        installments_object = Installments.objects.filter(user=self.request.user, pk=self.kwargs['pk']).first()
        if installments_object:
            installment_payment_object = form.save(commit=False)
            installment_payment_object.installment = installments_object
            if installments_object.get_payment_remaining_number() - 1 <= 0:
                installments_object.status = "CLS"
                installments_object.save()
        return super(PaymentInstallmentView, self).form_valid(form)
