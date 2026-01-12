from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Данные о странах
COUNTRIES = {
    'japan': {
        'name': 'Япония',
        'description': 'Автомобили из Японии - это качество, надежность и передовые технологии. Мы предлагаем широкий выбор японских автомобилей различных марок.',
        'features': ['Высокое качество', 'Надежность', 'Передовые технологии', 'Широкий выбор марок']
    },
    'korea': {
        'name': 'Корея',
        'description': 'Корейские автомобили сочетают в себе современный дизайн, отличное качество и доступные цены. Популярные марки: Hyundai, Kia, Genesis.',
        'features': ['Современный дизайн', 'Отличное качество', 'Доступные цены', 'Популярные марки']
    },
    'china': {
        'name': 'Китай',
        'description': 'Китайские автомобили - это отличное соотношение цены и качества. Мы предлагаем автомобили ведущих китайских производителей.',
        'features': ['Отличное соотношение цены и качества', 'Современные технологии', 'Широкий модельный ряд', 'Доступные цены']
    }
}

# Примеры автомобилей
CARS = [
    {
        'id': 1,
        'brand': 'Toyota',
        'model': 'Camry',
        'year': 2023,
        'country': 'japan',
        'price': '2 500 000',
        'image': 'https://via.placeholder.com/400x300?text=Toyota+Camry'
    },
    {
        'id': 2,
        'brand': 'Honda',
        'model': 'CR-V',
        'year': 2023,
        'country': 'japan',
        'price': '2 800 000',
        'image': 'https://via.placeholder.com/400x300?text=Honda+CR-V'
    },
    {
        'id': 3,
        'brand': 'Hyundai',
        'model': 'Tucson',
        'year': 2023,
        'country': 'korea',
        'price': '2 200 000',
        'image': 'https://via.placeholder.com/400x300?text=Hyundai+Tucson'
    },
    {
        'id': 4,
        'brand': 'Kia',
        'model': 'Sportage',
        'year': 2023,
        'country': 'korea',
        'price': '2 300 000',
        'image': 'https://via.placeholder.com/400x300?text=Kia+Sportage'
    },
    {
        'id': 5,
        'brand': 'Geely',
        'model': 'Coolray',
        'year': 2023,
        'country': 'china',
        'price': '1 800 000',
        'image': 'https://via.placeholder.com/400x300?text=Geely+Coolray'
    },
    {
        'id': 6,
        'brand': 'Chery',
        'model': 'Tiggo 8',
        'year': 2023,
        'country': 'china',
        'price': '1 900 000',
        'image': 'https://via.placeholder.com/400x300?text=Chery+Tiggo+8'
    }
]

@app.route('/')
def index():
    return render_template('index.html', countries=COUNTRIES, cars=CARS[:6])

@app.route('/country/<country_code>')
def country(country_code):
    if country_code not in COUNTRIES:
        flash('Страна не найдена', 'error')
        return redirect(url_for('index'))
    
    country_cars = [car for car in CARS if car['country'] == country_code]
    return render_template('country.html', 
                         country=COUNTRIES[country_code], 
                         country_code=country_code,
                         cars=country_cars)

@app.route('/car/<int:car_id>')
def car_detail(car_id):
    car = next((c for c in CARS if c['id'] == car_id), None)
    if not car:
        flash('Автомобиль не найден', 'error')
        return redirect(url_for('index'))
    
    country_info = COUNTRIES[car['country']]
    return render_template('car_detail.html', car=car, country=country_info)

@app.route('/catalog')
def catalog():
    return render_template('catalog.html', cars=CARS, countries=COUNTRIES)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        
        if name and email and message:
            # Здесь можно добавить отправку email или сохранение в БД
            flash('Спасибо за ваше сообщение! Мы свяжемся с вами в ближайшее время.', 'success')
            return redirect(url_for('contact'))
        else:
            flash('Пожалуйста, заполните все обязательные поля.', 'error')
    
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

