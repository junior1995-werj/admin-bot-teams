from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .handler import AccessedCard, Card
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django_auth_ldap.backend import LDAPBackend


@login_required(login_url="/")
def index(request): 
    ac = AccessedCard()
    list_values, list_days = ac.get_total_last_ten_days()
    year, year_value, percent_year, list_years, list_years_values = ac.get_total_year()
    month_return, month_value_return, list_month_values, percent_month = ac.get_total_month()
    list_card_quantity = ac.get_main_questions()

    context = {
        "list_values_days": list_values,
        "list_days": list_days,
        "year": year,
        "year_value": year_value,
        "percent_year": percent_year,
        "list_years": list_years,
        "list_years_values": list_years_values,
        "month_return": month_return,
        "month_value_return": month_value_return,
        "list_month_values": list_month_values,
        "percent_month": percent_month,
        "list_card_quantity": list_card_quantity,
    }


    return render(request=request, template_name="index.html", context=context)

@login_required(login_url="/")
def mensagens_cadastradas(request):
    card = Card()
    list_cards = card.get_cards()
    context = {"list_cards": list_cards}
    return render(request=request, template_name="mensagens_cadastradas.html", context=context)

@login_required(login_url="/")
def criar_mensagem(request):
    return render(
        request=request,
        template_name="criar_mensagem.html"
    )

@login_required(login_url="/")
def create(request):
    card = Card()
    if request.method == "POST":
        card.create(request.POST)

    return HttpResponseRedirect("/mensagens_cadastradas")

@login_required(login_url="/")
def update(request, id):
    card = Card()
    if request.method == "POST":
        card.update(form=request.POST, id=id)

    return HttpResponseRedirect("/mensagens_cadastradas")

@login_required(login_url="/")
def edit_config(request, id):
    card = Card()
    dict_card = card.get_card_by_id(id)

    for i in range(0,len(dict_card['description']['description'])):
        dict_card['description']['description'][i]['index'] = i

    context = {"dict_card": dict_card, "description": dict_card['description']['description']}
    return render(
        request=request,
        template_name="edit_config.html",
        context=context
    )


def autenticate(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        #teste = LDAPBackend().authenticate(username=username ,password=password, request=request)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/index")
        else:
            messages.add_message(request, messages.INFO, "Username ou Senha incorreto")
        
    return render(
        request,
        "authentication-login.html"
    )