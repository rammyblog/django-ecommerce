from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
	user = models.ForeignKey('auth.User', related_name='user', on_delete = models.CASCADE)
	first_name = models.CharField(max_length = 250, blank=True, null=True)
	last_name = models.CharField(max_length = 250, blank=True, null=True)
	about = models.TextField(max_length = 10000)
	address = models.CharField(max_length=250)
	additional_info = models.CharField(max_length=250, blank=True, null=True)
	city = models.CharField(max_length = 50, blank = True)
	default_address = models.BooleanField(default=False)
	postal_code=models.CharField(max_length=50)
	phone = models.PositiveIntegerField(default = 0)
	phone2 = models.PositiveIntegerField(default = 0, blank=True, null=True)
	

	def __str__(self):
		return self.user.username 

	def defaultAddress(self):
		self.default_address=True
		self.save()
	
	def removeDefault(self):
		self.default_address=False
		self.save()
	
	

def user_post_save(sender, **kwargs):
	if kwargs['created']:
		user_profile = UserProfile.objects.create(user=kwargs['instance'], default_address=True)

post_save.connect(user_post_save, sender=User)
