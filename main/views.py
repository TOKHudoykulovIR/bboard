from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import AdvUser
from .forms import ChangeUserlnfoForm, RegisterUserForm
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature 
from .utilities import signer
from django.contrib.auth import logout
from django.contrib import messages




class DeleteUserView(LoginRequiredMixin, DeleteView):
	model = AdvUser
	template_name = 'main/delete_user.html'
	success_url = reverse_lazy('main:index')

	def setup(self, request, *args, **kwargs):  # этот метод setup() сохранили ключ текущего пользователя,
		self.user_id = request.user.pk
		return super().setup(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):  # перед удалением текущего юзеар нужно выполнить выход, это сделает метод post() + всплывающее сообщение
		logout(request)
		messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
		return super().post(request, *args, **kwargs)

	def get_object(self, queryset=None):  # этот метод get_object() отыскал по ключу (сохр-ный в setup() методе) пользователя, подлежащего удалению.
		if not queryset:
			queryset = self.get_queryset()
		return get_object_or_404(queryset, pk = self.user_id)



def user_activate(request, sign):
	try:
		username = signer.unsign(sign)
	except BadSignature:  # чтобы проверить были ли изменены как-то подпись или значение использ BadSignature
		return render(request, 'main/bad_signature.html')
	user = get_object_or_404(AdvUser, username=username)
	if user.is_activated:
		template = 'main/user_is_activated.html'
	else:
		template = 'main/activation_done.html'
		user.is_active = True
		user.is_activated = True
		user.save()
	return render(request, template)


class RegisterDoneView(TemplateView):
	template_name = 'main/register_done.html'


class RegisterUserView(CreateView):
	model = AdvUser
	template_name = 'main/register_user.html'
	form_class = RegisterUserForm
	success_url = reverse_lazy('main:register_done')


class BBPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
	template_name = 'main/password_change.html'
	success_url = reverse_lazy('main:profile')
	success_message = 'Пароль пользоваетля изменен'


class ChangeUserlnfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
	model = AdvUser
	template_name = 'main/change_user_info.html'  # путь к файлу шаблона, создающего страницу с формой
	form_class = ChangeUserlnfoForm  # ссылка на класс формы, связанной с моделью
	success_url = reverse_lazy('main:profile')  # интернет-адрес для перенаправления после успешного сохранения данных. reverse_lazy() принимает имя маршрута и значения всех входящих в маршрут URL-параметров(если есть). Результат - готовый интернет-адрес.
	success_message = 'Данные пользоваетля изменены'

	def setup(self, request, *args, **kwargs):
		self.user_id = request.user.pk
		return super().setup(request, *args, **kwargs)

	def get_object(self, queryset=None):
		if not queryset:
			queryset = self.get_queryset()
		return get_object_or_404(queryset, pk=self.user_id)


class BBLogoutView(LoginRequiredMixin, LogoutView): #Стр выхода должна быть доступна только зареганным юзерам, выполнившим вход. Поэтому мы добавили в число суперклассов контроллера-класса BBLogoutView примесь LoginRequiredMixin. 
	template_name = 'main/logout.html'


@login_required
def profile(request):
	return render(request, 'main/profile.html')


class BBLoginView(LoginView):
	template_name='main/login.html'


def other_page(request, page):
	try:
		template = get_template('main/' + page + '.html')
	except TemplateDoesNotExist:
		raise Http404
	return HttpResponse(template.render(request=request))


def index(request):
	return render(request, 'main/index.html')





















