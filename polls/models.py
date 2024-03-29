import datetime
from django.utils import timezone
from django.db import models

# Create your models here.

class Poll(models.Model):
	question = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

	def __unicode__(self):
		return self.question

	def was_published_recently(self):
		dia_de_hoje = timezone.now()
		um_dia = datetime.timedelta(days=1)
		ontem = dia_de_hoje - um_dia

		#return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
		return self.pub_date >= ontem 
	was_published_recently.admin_order_field = 'pub_date'
	was_published_recently.boolean = True
	was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
	poll = models.ForeignKey(Poll)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __unicode__(self):
		return self.choice_text
