from django.db import models

class Table(models.Model):
    number = models.IntegerField(unique=True)
    seats = models.IntegerField(default=4)  # Указываем значение по умолчанию

    def __str__(self):
        return f"Столик {self.number} ({self.seats} мест)"
