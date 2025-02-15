from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    release_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.model})"


class NetworkNode(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    email = models.EmailField(verbose_name='Почта')
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house_number = models.CharField(max_length=10, verbose_name='Номер дома')
    products = models.ManyToManyField(Product)
    supplier = models.CharField(max_length=100, null=True, blank=True, verbose_name='Поставщик (предыдущий по иерархии объект сети)')
    debt = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Задолженность перед поставщиком в денежном выражении с точностью до копеек')
    level = models.IntegerField(verbose_name='Уровень в иерархии')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
