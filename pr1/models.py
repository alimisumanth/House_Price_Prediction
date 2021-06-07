from django.db import models

# user db
class User(models.Model):
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=50)
	email = models.EmailField(null=True)

	def __str__(self):
		return self.username

class Upload(models.Model):
	upload_file = models.FileField()