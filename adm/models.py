from django.db import models

# Create your models here.


class CardModel(models.Model):
    

    id = models.IntegerField(primary_key=True, db_index=True)
    tittle = models.CharField(max_length=255, db_index=True)
    description = models.TextField(db_index=True) 
    recurring_send = models.BooleanField(default=False) 
    card_options = models.BooleanField(default=True) 
    last_update = models.DateTimeField()
    created_at = models.DateTimeField()
    team = models.CharField(max_length=255)
    status = models.BooleanField() 

    class Meta:
        managed = False
        db_table = "bot_agility_card"

class AccessedCardModel(models.Model): 

    id = models.IntegerField(primary_key=True, db_index=True)
    username = models.CharField(max_length=255)
    id_card = models.CharField(max_length=255)
    date_accessed = models.DateTimeField(null=True, blank=True)

    class Meta:
        
        db_table = "bot_agility_accessed_card"
