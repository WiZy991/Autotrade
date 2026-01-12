from django.db import models
from django.urls import reverse


class Country(models.Model):
    """Модель для стран (Япония, Корея, Китай)"""
    name = models.CharField('Название', max_length=100)
    code = models.SlugField('Код', unique=True, help_text='japan, korea, china')
    description = models.TextField('Описание', blank=True)
    flag_emoji = models.CharField('Эмодзи флага', max_length=10, default='🇯🇵')
    
    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class CarType(models.Model):
    """Модель для типов кузова (седан, хэчбек, кроссовер и т.д.)"""
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('URL', unique=True)
    description = models.TextField('Описание', blank=True)
    
    class Meta:
        verbose_name = 'Тип кузова'
        verbose_name_plural = 'Типы кузова'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Car(models.Model):
    """Модель для автомобилей"""
    brand = models.CharField('Марка', max_length=100)
    model = models.CharField('Модель', max_length=100)
    year = models.IntegerField('Год выпуска')
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='cars',
        verbose_name='Страна'
    )
    car_type = models.ForeignKey(
        CarType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cars',
        verbose_name='Тип кузова'
    )
    price = models.DecimalField('Цена', max_digits=12, decimal_places=2)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Главное изображение', upload_to='cars/', blank=True, null=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    is_active = models.BooleanField('Активен', default=True)
    
    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"
    
    def get_absolute_url(self):
        return reverse('car_detail', kwargs={'pk': self.pk})


class CarImage(models.Model):
    """Модель для дополнительных изображений автомобиля"""
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Автомобиль'
    )
    image = models.ImageField('Изображение', upload_to='cars/gallery/')
    alt_text = models.CharField('Альтернативный текст', max_length=200, blank=True)
    order = models.IntegerField('Порядок', default=0)
    
    class Meta:
        verbose_name = 'Изображение автомобиля'
        verbose_name_plural = 'Изображения автомобилей'
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.car} - изображение {self.order}"

