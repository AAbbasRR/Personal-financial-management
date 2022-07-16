from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from .models import NotificationOptions
from .forms import NotificationOptionsCreateForm


class NotificationOptionCreateListView(LoginRequiredMixin, CreateView):
    model = NotificationOptions
    form_class = NotificationOptionsCreateForm
    template_name = 'panel/options.html'
    success_url = reverse_lazy('Options:listnotificationoption')

    def form_valid(self, form):
        notification_obj = form.save(commit=False)
        notification_obj.user = self.request.user
        return super(NotificationOptionCreateListView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(NotificationOptionCreateListView, self).get_context_data(**kwargs)
        notifications = NotificationOptions.objects.filter(user=self.request.user)
        context['notification_list'] = {
            "check": notifications.filter(type="CHK").first(),
            "installment": notifications.filter(type="INS").first(),
            "debtanddemand": notifications.filter(type="DBM").first(),
            "bill": notifications.filter(type="BIL").first(),
        }
        return context


class NotificationOptionUpdateView(LoginRequiredMixin, UpdateView):
    model = NotificationOptions
    form_class = NotificationOptionsCreateForm

    def get_success_url(self):
        return HttpResponseRedirect(reverse("Options:listnotificationoption"))

    def get_queryset(self):
        return NotificationOptions.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        form_notification = NotificationOptionsCreateForm(data=request.POST, instance=self.get_object())
        if form_notification.is_valid():
            form_notification.save()
            return self.get_success_url()


class NotificationOptionDeleteView(LoginRequiredMixin, DeleteView):
    model = NotificationOptions
    success_url = reverse_lazy("Options:listnotificationoption")

    def get_queryset(self):
        return NotificationOptions.objects.filter(user=self.request.user)

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
