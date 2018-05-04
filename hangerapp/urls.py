from django.conf.urls import include, url

from . import views

app_name = 'hangerapp'
urlpatterns = [
	url(r'^$', views.make_a_guess_sync, name='initial'),
	url(r'^async/', views.make_a_guess_async, name='async'),
	url(r'^asyncret/', views.get_secret, name='secret'),
	url(r'^language/', views.change_language, name='language'),
]