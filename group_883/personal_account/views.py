from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from personal_account.forms import UserLoginForm, UserRegisterForm, UserEditForm, CreateArticleForm
from mainapp.models import Article


def login(request):
    login_form = UserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('mainapp:index'))

    context = {
        'login_form': login_form
    }

    return render(request, 'personal_account/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('mainapp:index'))


def register(request):
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('mainapp:index'))
    else:
        register_form = UserRegisterForm()
    context = {
        'register_form': register_form
    }
    return render(request, 'personal_account/register.html', context)


def edit(request):
    if request.method == 'POST':
        edit_form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('personal_account:user'))
    else:
        edit_form = UserEditForm(instance=request.user)
    context = {
        'edit_form': edit_form
    }
    return render(request, 'personal_account/edit.html', context)


def user(request):
    return render(request, 'personal_account/user.html')


class ListArticle(ListView):
    model = Article
    template_name = 'personal_account/article_list.html'

    def get_queryset(self):
        return Article.objects.filter(user=self.request.user)


class CreateArticle(CreateView):
    model = Article
    template_name = 'personal_account/article_create.html'
    form_class = CreateArticleForm

    def get_success_url(self):
        return reverse('personal_account:list_article')


class EditArticle(UpdateView):
    model = Article
    template_name = 'personal_account/article_edit.html'
    form_class = CreateArticleForm

    def get_success_url(self):
        return reverse('personal_account:list_article')


class DeleteArticle(DeleteView):
    model = Article
    template_name = 'personal_account/article_delete.html'

    def get_success_url(self):
        return reverse('personal_account:list_article')
