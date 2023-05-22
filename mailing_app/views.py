from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DetailView, ListView, DeleteView

from mailing_app.models import Mailing, Client


class ClientListView(ListView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    fields = ('email', 'full_name', 'comments')
    success_url = reverse_lazy('mailing_app:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('email', 'full_name', 'comments')
    success_url = reverse_lazy('mailing_app:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing_app:client_list')


class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    fields = ('mailing_time', 'frequency', 'message', 'clients')
    success_url = reverse_lazy('mailing_app:mailing_list')


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ('mailing_time', 'frequency', 'mailing_status', 'message', 'clients')
    success_url = reverse_lazy('mailing_app:mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing_app:mailing_list')
