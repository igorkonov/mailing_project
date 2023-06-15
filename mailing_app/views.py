from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DetailView, ListView, DeleteView

from mailing_app.forms import MailingForm
from mailing_app.models import Mailing, Client, Message, MailingAttempt


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user_id=self.request.user)
        if self.request.user.has_perm('mailing_app.set_mailing_status'):
            return queryset

        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ('email', 'full_name', 'comments')
    success_url = reverse_lazy('mailing_app:client_list')

    def form_valid(self, form):
        client = form.save()
        client.user = self.request.user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(UserPassesTestMixin, UpdateView):
    model = Client
    fields = ('email', 'full_name', 'comments')
    success_url = reverse_lazy('mailing_app:client_list')

    def test_func(self):
        client = self.get_object()
        user = self.request.user
        return user.is_authenticated and (client.user == user or user.has_perm('mailing_app.change_client'))


class ClientDeleteView(UserPassesTestMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing_app:client_list')

    def test_func(self):
        client = self.get_object()
        user = self.request.user
        return user.is_authenticated and (client.user == user or user.has_perm('mailing_app.delete_client'))


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user_id=self.request.user)
        if self.request.user.has_perm('mailing_app.view_mailing'):
            return queryset

        return queryset.filter(user=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.has_perm('mailing_app.view_mailing') or self.request.user == self.object.user:
            return self.object
        raise HttpResponseForbidden


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing_app:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['clients'].queryset = Client.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        mailing = form.save()
        mailing.user = self.request.user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(UserPassesTestMixin, UpdateView):
    model = Mailing
    fields = '__all__'
    success_url = reverse_lazy('mailing_app:mailing_list')

    def test_func(self):
        mailing = self.get_object()
        user = self.request.user
        return user.is_authenticated and (mailing.user == user or user.has_perm('mailing_app.change_mailing'))


class MailingDeleteView(UserPassesTestMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing_app:mailing_list')

    def test_func(self):
        mailing = self.get_object()
        user = self.request.user
        return user.is_authenticated and (mailing.user == user or user.has_perm('mailing_app.delete_mailing'))


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user_id=self.request.user)
        if self.request.user.has_perm('mailing_app.set_mailing_status'):
            return queryset

        return queryset


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ('subject', 'body',)
    success_url = reverse_lazy('mailing_app:message_list')

    def form_valid(self, form):
        message = form.save()
        message.user = self.request.user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(UserPassesTestMixin, UpdateView):
    model = Message
    fields = ('subject', 'body',)
    success_url = reverse_lazy('mailing_app:message_list')

    def test_func(self):
        message = self.get_object()
        user = self.request.user
        return user.is_authenticated and (message.user == user or user.has_perm('mailing_app.change_message'))


class MessageDeleteView(UserPassesTestMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing_app:message_list')

    def test_func(self):
        message = self.get_object()
        user = self.request.user
        return user.is_authenticated and (message.user == user or user.has_perm('mailing_app.delete_message'))


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = 'mailing_app/mailing_attempt_list.html'

