from django.db import models


# user db
class User(models.Model):
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=50)
	email = models.EmailField(null=True)
	mobile = models.CharField(max_length=15, null=True)

	def __str__(self):
		return self.username
