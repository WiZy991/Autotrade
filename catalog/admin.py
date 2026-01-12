from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Country, CarType, Car, CarImage


class CarImageInline(admin.TabularInline):
    """Инлайн для изображений автомобиля"""
    model = CarImage
    extra = 1
    fields = ('image', 'image_preview', 'alt_text', 'order')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "Загрузите изображение"
    image_preview.short_description = 'Превью'


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('flag_emoji', 'name', 'code', 'car_count', 'view_cars_link')
    list_filter = ('name',)
    search_fields = ('name', 'code', 'description')
    prepopulated_fields = {'code': ('name',)}
    list_display_links = ('name',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'code', 'flag_emoji', 'description')
        }),
    )
    
    def car_count(self, obj):
        count = obj.cars.count()
        if count > 0:
            return format_html('<span style="color: #28a745; font-weight: bold;">{}</span>', count)
        return format_html('<span style="color: gray;">{}</span>', count)
    car_count.short_description = 'Автомобилей'
    
    def view_cars_link(self, obj):
        count = obj.cars.count()
        if count > 0:
            url = reverse('admin:catalog_car_changelist') + f'?country__id__exact={obj.id}'
            return format_html('<a href="{}" class="button">Просмотреть ({})</a>', url, count)
        return "-"
    view_cars_link.short_description = 'Действия'


@admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'car_count', 'view_cars_link')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ('name',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'description')
        }),
    )
    
    def car_count(self, obj):
        count = obj.cars.count()
        if count > 0:
            return format_html('<span style="color: #28a745; font-weight: bold;">{}</span>', count)
        return format_html('<span style="color: gray;">{}</span>', count)
    car_count.short_description = 'Автомобилей'
    
    def view_cars_link(self, obj):
        count = obj.cars.count()
        if count > 0:
            url = reverse('admin:catalog_car_changelist') + f'?car_type__id__exact={obj.id}'
            return format_html('<a href="{}" class="button">Просмотреть ({})</a>', url, count)
        return "-"
    view_cars_link.short_description = 'Действия'


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('image_thumbnail', 'brand', 'model', 'year', 'country', 'car_type', 'price_formatted', 'is_active', 'is_active_badge', 'created_at')
    list_filter = ('country', 'car_type', 'year', 'is_active', 'created_at')
    search_fields = ('brand', 'model', 'description')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    inlines = [CarImageInline]
    list_per_page = 25
    list_editable = ('is_active',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('brand', 'model', 'year', 'country', 'car_type', 'price')
        }),
        ('Описание', {
            'fields': ('description',),
            'classes': ('wide',)
        }),
        ('Изображения', {
            'fields': ('image', 'image_preview')
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return format_html('<span style="color: gray;">Нет фото</span>')
    image_thumbnail.short_description = 'Фото'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 300px; max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.2);" />',
                obj.image.url
            )
        return format_html('<p style="color: gray; padding: 20px;">Нет изображения</p>')
    image_preview.short_description = 'Превью изображения'
    
    def price_formatted(self, obj):
        price_value = f"{int(obj.price):,}".replace(",", " ")
        return format_html('<strong style="color: #28a745;">{} ₽</strong>', price_value)
    price_formatted.short_description = 'Цена'
    price_formatted.admin_order_field = 'price'
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;">АКТИВЕН</span>')
        return format_html('<span style="background: #dc3545; color: white; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;">НЕ АКТИВЕН</span>')
    is_active_badge.short_description = 'Статус'
    is_active_badge.admin_order_field = 'is_active'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('country', 'car_type')
