from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Car, Country, CarType


def index(request):
    """Главная страница"""
    countries = Country.objects.all()
    featured_cars = Car.objects.filter(is_active=True)[:6]
    
    context = {
        'countries': countries,
        'cars': featured_cars,
    }
    return render(request, 'index.html', context)


def catalog_view(request):
    """Каталог автомобилей с фильтрацией"""
    cars = Car.objects.filter(is_active=True)
    countries = Country.objects.all()
    car_types = CarType.objects.all()
    
    # Фильтрация по стране
    country_filter = request.GET.get('country')
    if country_filter:
        cars = cars.filter(country__code=country_filter)
    
    # Фильтрация по типу кузова
    type_filter = request.GET.get('type')
    if type_filter:
        cars = cars.filter(car_type__slug=type_filter)
    
    # Поиск
    search_query = request.GET.get('search')
    if search_query:
        cars = cars.filter(
            Q(brand__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Пагинация: показываем первые 20 машин
    cars_per_page = 20
    total_cars = cars.count()
    cars = cars[:cars_per_page]
    has_more = total_cars > cars_per_page
    
    context = {
        'cars': cars,
        'countries': countries,
        'car_types': car_types,
        'selected_country': country_filter,
        'selected_type': type_filter,
        'search_query': search_query,
        'has_more': has_more,
        'total_cars': total_cars,
    }
    return render(request, 'catalog.html', context)


def load_more_cars(request):
    """AJAX endpoint для загрузки следующих машин"""
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    try:
        page = int(request.GET.get('page', 2))  # Начинаем с 2, так как первая страница уже загружена
        if page < 2:
            page = 2
    except (ValueError, TypeError):
        page = 2
    
    cars_per_page = 20
    offset = (page - 1) * cars_per_page
    
    cars = Car.objects.filter(is_active=True)
    
    # Применяем те же фильтры, что и в catalog_view
    country_filter = request.GET.get('country')
    if country_filter:
        cars = cars.filter(country__code=country_filter)
    
    type_filter = request.GET.get('type')
    if type_filter:
        cars = cars.filter(car_type__slug=type_filter)
    
    search_query = request.GET.get('search')
    if search_query:
        cars = cars.filter(
            Q(brand__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    total_cars = cars.count()
    cars = cars[offset:offset + cars_per_page]
    has_more = offset + cars_per_page < total_cars
    
    # Рендерим HTML для карточек
    html = render_to_string('catalog_car_cards.html', {'cars': cars}, request=request)
    
    return JsonResponse({
        'html': html,
        'has_more': has_more,
        'page': page + 1,
    })


def country_view(request, country_code):
    """Страница страны"""
    country = get_object_or_404(Country, code=country_code)
    cars = Car.objects.filter(country=country, is_active=True)
    
    context = {
        'country': country,
        'country_code': country_code,
        'cars': cars,
    }
    return render(request, 'country.html', context)


def car_detail(request, pk):
    """Детальная страница автомобиля"""
    car = get_object_or_404(Car, pk=pk, is_active=True)
    
    context = {
        'car': car,
        'country': car.country,
    }
    return render(request, 'car_detail.html', context)


def about(request):
    """Страница о нас"""
    return render(request, 'about.html')


def contact(request):
    """Страница контактов"""
    if request.method == 'POST':
        # Здесь можно добавить обработку формы
        pass
    return render(request, 'contact.html')

