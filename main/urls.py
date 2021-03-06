from django.urls import path
from .views import (
	index, 
	other_page,
	BBLoginView,
	profile,
	BBLogoutView,
	ChangeUserlnfoView,
	BBPasswordChangeView,
	RegisterUserView,
	RegisterDoneView,
	user_activate,
	DeleteUserView,
	)


app_name = 'main'

urlpatterns = [
	path('', index, name='index'),
	path('<str:page>/', other_page, name='other'),
	path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
	path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
	path('accounts/register/', RegisterUserView.as_view(), name='register'),
	path('accounts/login/', BBLoginView.as_view(), name='login'),
	path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
	path('accounts/profile/change/', ChangeUserlnfoView.as_view(), name = 'profile_change'),
	path('accounts/profile/', profile, name='profile'),
	path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
	path('accounts/password/change/', BBPasswordChangeView.as_view(), name='password_change'),
]