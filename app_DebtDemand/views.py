from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from .forms import DebtDemandCreateForm
from .models import DebtAndDemand


class DebtDemandCreateListView(LoginRequiredMixin, CreateView):
    model = DebtAndDemand
    form_class = DebtDemandCreateForm
    template_name = "panel/debtdemand.html"
    success_url = reverse_lazy("DebtDemand:listdebtdamends")

    def form_valid(self, form):
        installments = form.save(commit=False)
        installments.user = self.request.user
        return super(DebtDemandCreateListView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DebtDemandCreateListView, self).get_context_data(**kwargs)
        context['debt_list'] = {
            "opened": DebtAndDemand.objects.filter(user=self.request.user, type="DEB", status="OPN"),
            "closed": DebtAndDemand.objects.filter(user=self.request.user, type="DEB", status="CLS"),
        }
        context['demand_list'] = {
            "opened": DebtAndDemand.objects.filter(user=self.request.user, type="DEM", status="OPN"),
            "closed": DebtAndDemand.objects.filter(user=self.request.user, type="DEM", status="CLS"),
        }
        return context


class DebtDemandCloseView(LoginRequiredMixin, UpdateView):
    model = DebtAndDemand
    success_url = reverse_lazy("DebtDemand:listdebtdamends")

    def get_success_url(self):
        return HttpResponseRedirect(reverse("DebtDemand:listdebtdamends"))

    def get_queryset(self):
        return DebtAndDemand.objects.filter(user=self.request.user, status="OPN")

    def get(self, request, *args, **kwargs):
        debt_demand_object = self.get_object()
        if debt_demand_object:
            debt_demand_object.status = "CLS"
            debt_demand_object.end_date = timezone.now()
            debt_demand_object.save()
            return self.get_success_url()


class DebtDemandDeleteView(LoginRequiredMixin, DeleteView):
    model = DebtAndDemand
    success_url = reverse_lazy("DebtDemand:listdebtdamends")

    def get_queryset(self):
        return DebtAndDemand.objects.filter(user=self.request.user)

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
