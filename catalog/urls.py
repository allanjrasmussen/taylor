from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^adduser/$', views.adduser, name='adduser'),
    url(r'^login/$', auth_views.login,  name='login'),
    url(r'^logout/$', auth_views.logout,  name='logout'),
    url(r'^password_reset_form/$', auth_views.password_reset, name='password_reset_form'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^profile/', views.profile, name='profile'),

]

# USERS page left menu
urlpatterns += [
    url(r'^measurements/', views.measurements, name='measurements'),
    url(r'^clients', views.clients, name='clients'),
    url(r'^client/(?P<pk>\d+)$', views.ClientDetailView.as_view(), name='client-detail'),
    url(r'^klient', views.klient_gemt, name='klient_gemt'),
    url(r'^purchases', views.purchases, name='purchases'),
    url(r'^person', views.person, name='person'),
    url(r'^navgoco/', views.navgoco, name='navgoco'),
]

# [Basic Blocks] dropdown menu
urlpatterns += [

    url(r'^drop01/', views.drop01_view_all, name='drop01'),
    url(r'^drop01_dress_block/', views.drop01_dress_block, name='drop01_dress_block'),
    url(r'^drop01_dress_sleeve/', views.drop01_dress_sleeve, name='drop01_dress_sleeve'),
    url(r'^drop01_shirt_sweatshirt/', views.drop01_shirt_sweatshirt, name='drop01_shirt_sweatshirt'),
    url(r'^drop01_shirt_sleeve/', views.drop01_shirt_sleeve, name='drop01_shirt_sleeve'),
    url(r'^drop01_sweatshirt_sleeve/', views.drop01_sweatshirt_sleeve, name='drop01_sweatshirt_sleeve'),
    url(r'^drop01_skirt_block/', views.drop01_skirt_block, name='drop01_skirt_block'),
    url(r'^drop01_trouser_block/', views.drop01_trouser_block, name='drop01_trouser_block'),
    url(r'^drop01_coat_block/', views.drop01_coat_block, name='drop01_coat_block'),
    url(r'^drop01_jacket_block/', views.drop01_jacket_block, name='drop01_jacket_block'),
]

# [Variation of Basic] dropdown menu
urlpatterns += [

]

# [Pattern Cutting] dropdown menu
urlpatterns += [

]


# [New & Projects] dropdown menu
urlpatterns += [

]

# [The Studio] dropdown menu
urlpatterns += [
    url(r'^about/', views.about, name='about'),
    url(r'^drop05_how2_meas/', views.drop05_how2_meas, name='drop05_how2_meas'),
]
