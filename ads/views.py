from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import Ad, Category
from .forms import AdForm
from django_filters.views import FilterView
from .filters import AdFilter

class AdListView(FilterView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    filterset_class = AdFilter
    paginate_by = 10

class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'

class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ad_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class AdUpdateView(LoginRequiredMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'

    def get_queryset(self):
        return Ad.objects.filter(author=self.request.user)

class AdDeleteView(LoginRequiredMixin, DeleteView):
    model = Ad
    success_url = reverse_lazy('ad_list')
    template_name = 'ads/ad_confirm_delete.html'

    def get_queryset(self):
        return Ad.objects.filter(author=self.request.user)