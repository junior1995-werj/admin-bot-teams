from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path("index/", views.index, name="index"),
    path("mensagens_cadastradas/", views.mensagens_cadastradas, name="mensagens_cadastradas"),
    path("criar_mensagem/", views.criar_mensagem, name="criar_mensagem"),
    path("mensagens_cadastradas/edit_config/<int:id>", views.edit_config, name="edit_config"),
    path("update/<int:id>", views.update, name="update"),
    path("create/", views.create, name="create"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("", views.autenticate, name="autenticate"),
]