
import ast
from datetime import datetime, timedelta
from .models import AccessedCardModel, CardModel
from django.db.models import Count, DateField
from django.db.models.functions import Cast, Extract

class AccessedCard:     

    def get_total_last_ten_days(self):
        data = datetime.now()
        data_anterior = data - timedelta(days=10)

        card_total_days = AccessedCardModel.objects.filter(date_accessed__gte=data_anterior).annotate(date_accessed_date=Cast("date_accessed", output_field=DateField())).values('date_accessed_date').annotate(id_count=Count('id')).order_by("date_accessed_date").all()[:10]

        list_return_dates = []
        list_return_values = []
        for day in card_total_days: 
            
            list_return_values.append(day['id_count'])
            list_return_dates.append(day['date_accessed_date'].strftime("%d-%m-%Y"))

        return list_return_values, list_return_dates
        
    def get_total_year(self):
        data = datetime.now()
        year_today = datetime(day=1, month=1, year=(data.year-1))

        list_total_years = AccessedCardModel.objects.values('date_accessed').annotate(id_count=Count('id'))

        list_total_years = self._calculate_values_in_years(list_total_years,"year")

        list_years = []
        list_values = []
        year_return = 0
        year_value_return = 0

        for ano, total in list_total_years.items(): 
            if ano == data.year:
                year_return = data.year
                year_value_return = total
            
            list_years.append(ano)
            list_values.append(total)

        percent = self._calculate_value_percent_year(list_total_years)

        return year_return, year_value_return, percent, list_years, list_values

    def get_total_month(self):

        data = datetime.now()
        date_year = datetime(day=1, month=1, year=data.year)
        month_current = data.month

        list_month_by_current_year = AccessedCardModel.objects.filter(date_accessed__gte=date_year).values('date_accessed').annotate(id_count=Count('id')).order_by('date_accessed')
        
        list_month_by_current_year = self._calculate_values_in_years(list_month_by_current_year,"month")

        list_month_values = []
        month_return = ""
        month_value_return = 0

        for month, total in list_month_by_current_year.items(): 
            if month == month_current:
                month_return = month_current
                month_value_return = total

            list_month_values.append(total)

        percent = self._calculate_value_percent_month(list_month_by_current_year, month_current)

        return month_return, month_value_return, list_month_values, percent

    def get_main_questions(self): 
        data = datetime.now()
        date_year = datetime(day=1, month=1, year=data.year)
        month_current = data.month

        list_quantity_card_id = AccessedCardModel.objects.filter(date_accessed__gte=date_year).values('id_card').annotate(count=Count('id')).order_by('-count')
        

        list_card_id = []
        for id in list_quantity_card_id: 
            list_card_id.append(id['id_card'])

        cards_list = CardModel.objects.filter(id__in=list_card_id)[:5]

        list_return = []

        for card in cards_list:
            for quanity in list_quantity_card_id:
                if quanity['id_card'] == str(card.id):
                    list_return.append({
                        "tittle" : card.tittle,
                        "team": card.team,
                        "quantity": quanity['count']
                    })
                else:
                    continue
        return list_return

    @staticmethod
    def _calculate_value_percent_year(list_values:dict): 
        data = datetime.now()
        len_list = len(list_values)
        year = data.year
       

        if len_list == 1: 
            return int(((list_values[year] - 0)/ 1) * 100)
        
        else: 
            current_year = [0,0]
            last_year = [0,0]
            for ano, value in list_values.items():
                if ano == (year -1):
                    last_year = value
                elif ano == year:
                    current_year = value

            return round(((int(current_year) - int(last_year))/ int(last_year)) * 100)
    
    @staticmethod
    def _calculate_values_in_years(dados, method):
        total_por_ano = {}
        for item in dados:
            ano = None
            if method == "year":
                ano = item['date_accessed'].year 
            else: 
                ano = item['date_accessed'].month 
            id_count = item['id_count']
            
            if ano in total_por_ano.keys():
                total_por_ano[ano] += id_count
            else:
                total_por_ano[ano] = id_count

        return total_por_ano
    
    @staticmethod
    def _calculate_value_percent_month(list_values:dict, month):
        len_list = len(list_values)
        if len_list == 1: 
            key = list(list_values.keys())
            return int(((list_values[list(list_values.keys())[0]] - 0)/ 1) * 100)
        else: 
            month_average = 0 
            month_value = 0
            cont = 0
            for mes ,value in list_values.items():
                if int(mes) == month:
                    month_value = value
                else: 
                    cont +=1
                    month_average = round((month_average + value) / cont)

            return round(((month_value - month_average)/ month_average) * 100)
        

class Card: 

    def get_cards(self):
        cards = CardModel.objects.all()

        list_cards = []
        for card in cards: 
            list_cards.append(
                {
                    "id": card.id,
                    "tittle": card.tittle,
                    "description": card.description,
                    "recurring_send": card.recurring_send,
                    "card_options": card.card_options,
                    "last_update": card.last_update.date(),
                    "created_at": card.created_at.date(),
                    "team": card.team,
                    "status": card.status,
                }
            )
        return list_cards
    
    def get_card_by_id(self, id):
        card = CardModel.objects.filter(id=id).first()

        return {
            "id": card.id,
            "tittle": card.tittle,
            "description": ast.literal_eval(card.description) if card.description !="" else "",
            "recurring_send": card.recurring_send,
            "card_options": card.card_options,
            "team": card.team,
            "status": card.status,
        }

    def create(self, form):
        CardModel.objects.create(**self._get_forms_values(form, True))

    def update(self, form, id): 
        card = CardModel.objects.filter(id=id).first()
        dict_values = self._get_forms_values(form=form, new=False)
        card.tittle = dict_values['tittle']
        card.description = dict_values['description']
        card.status = dict_values['status']
        card.team = dict_values['team']
        card.last_update = datetime.now()
        card.recurring_send = dict_values['recurring_send']
        card.card_options = dict_values['card_options']
        card.save()


    def _get_forms_values(self, form, new) -> dict:
        tittle = form['tittle']
        team = form['team']
        card_options = True if 'card_options' in form.keys() else False
        recurring_send =  True if 'recurring_send' in form.keys() else False
        if new:
            status = True
        else:  
            status = True if 'status' in form.keys() else False
        return {
            "tittle":tittle,
            "description":str(self._get_description(form)), 
            "recurring_send":recurring_send,
            "card_options":card_options,
            "last_update":datetime.now(),
            "created_at":datetime.now(),
            "team":team,
            "status":status}

    @staticmethod
    def _get_description(form) -> dict:    
        description = {"description":[] }
        for value in sorted(form.keys()): 
            if value.startswith("description_"):
                description["description"].append({"description": form.values.__self__[value]})

        return description

