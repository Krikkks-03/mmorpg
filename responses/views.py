from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from accounts.tasks import send_email_task
from django.conf import settings
from .models import Response
from ads.models import Ad

class ResponseCreateView(LoginRequiredMixin, CreateView):
    model = Response
    fields = ['text']
    template_name = 'responses/response_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.ad = get_object_or_404(Ad, pk=self.kwargs['ad_pk'])
        if self.ad.author == request.user:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("Вы не можете откликнуться на своё объявление.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.ad = self.ad
        # Отправляем письмо автору объявления
        send_email_task.delay(
            subject='Новый отклик на ваше объявление',
            message=f'Пользователь {self.request.user.email} оставил отклик:\n{form.instance.text[:500]}',
            recipient_list=[self.ad.author.email]
        )
        return super().form_valid(form)

    def get_success_url(self):
        return self.ad.get_absolute_url()

class MyResponsesView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'responses/my_responses.html'
    paginate_by = 20

    def get_queryset(self):
        qs = Response.objects.filter(ad__author=self.request.user).select_related('ad', 'author')
        ad_id = self.request.GET.get('ad_id')
        if ad_id:
            qs = qs.filter(ad_id=ad_id)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_ads'] = Ad.objects.filter(author=self.request.user)
        return context

def accept_response(request, pk):
    response = get_object_or_404(Response, pk=pk, ad__author=request.user)
    response.is_accepted = True
    response.save()
    send_email_task.delay(
        subject='Ваш отклик принят!',
        message=f'Автор объявления "{response.ad.title}" принял ваш отклик.',
        recipient_list=[response.author.email]
    )
    return redirect('my_responses')

def delete_response(request, pk):
    response = get_object_or_404(Response, pk=pk, ad__author=request.user)
    response.delete()
    return redirect('my_responses')