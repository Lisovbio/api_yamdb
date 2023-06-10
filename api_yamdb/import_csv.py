import csv
import os

from api_yamdb.settings import BASE_DIR
from reviews.models import Category, Comment, Genre, Review, Titles, User

path = os.path.join(BASE_DIR, 'static/data/')
os.chdir(path)

# Скрипт импорта данных их category.csv в БД
with open('category.csv', mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        db = Category(
            id=row['id'],
            name=row['name'],
            slug=row['slug']
        )
        db.save()
    print('>>> Данные category загрузились успешно')

# Скрипт импорта данных их comments.csv в БД
with open('comments.csv', mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        db = Comment(
            id=row['id'],
            review=Review.objects.get(id=row['review_id']),
            text=row['text'],
            author=User.objects.get(id=row['author']),
            pub_date=row['pub_date']
        )
        db.save()
    print('>>> Данные comments загрузились успешно')

# Скрипт импорта данных их genre.csv в БД
with open('genre.csv', mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        db = Genre(
            id=row['id'],
            name=row['name'],
            slug=row['slug']
        )
        db.save()
    print('>>> Данные genre загрузились успешно')

# Скрипт импорта данных их review.csv в БД
with open('review.csv', mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        db = Review(
            id=row['id'],
            title=Titles.objects.get(id=row['title_id']),
            text=row['text'],
            author=User.objects.get(id=row['author']),
            score=row['score'],
            pub_date=row['pub_date']
        )
        db.save()
    print('>>> Данные review загрузились успешно')

# Скрипт импорта данных их titles.csv в БД
with open('titles.csv', mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        db = Titles(
            id=row['id'],
            name=row['name'],
            year=row['year'],
            category=Category.objects.get(id=row['category'])
        )
        db.save()
    print('>>> Данные titles загрузились успешно')

# Скрипт импорта данных их users.csv в БД
with open('users.csv', mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        db = User(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            role=row['role'],
            bio=row['bio'],
            first_name=row['first_name'],
            last_name=row['last_name']
        )
        db.save()
    print('>>> Данные users загрузились успешно')


"""
from .models import Category, Comment, Genre, Review, Titles, User

MODELS = {
    'categories': Category,
    'comments': Comment,
    'genre_titles': Titles,
    'genres': Genre,
    'reviews': Review,
    'titles': Titles,
    'users': User
}

csv_file_paths = {
    'path': f'/api_yamdb/static/data/{file}.csv' for file in MODELS
}

with open(csv_file_paths, encoding='utf-8', mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        Category.objects.get_or_create()
"""
