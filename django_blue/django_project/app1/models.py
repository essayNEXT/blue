from django.db import models


class User(models.Model):
    name_ukr = models.CharField(max_length=20, blank=False)
    surname_ukr = models.CharField(max_length=30, blank=False)
    patronymic_ukr = models.CharField(max_length=20, blank=False)
    name_en = models.CharField(max_length=20)
    surname_en = models.CharField(max_length=30)
    gender= models.CharField(max_length=9, blank=False)
    date_of_birth=models.DateField()
    email=models.EmailField()
    phone=models.CharField(max_length=20)
    telegram_id=models.CharField(max_length=20)
    status=models.CharField(max_length=9, blank=False)

    def __str__(self):
        return f'{self.surname_ukr} {self.name_ukr}'
