from django.contrib import admin

from .models import CardModel
from .models import AccessedCardModel

class CardAdmin(admin.ModelAdmin):
    list_display =  ['id', 'tittle', 'card_options', 'recurring_send', 'last_update', 'created_at', 'team', 'status']

admin.site.register(CardModel, CardAdmin)

class AccessedCardAdmin(admin.ModelAdmin):
    list_display =  ['username', 'id_card', 'date_accessed']

admin.site.register(AccessedCardModel, AccessedCardAdmin)