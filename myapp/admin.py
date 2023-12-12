from django.contrib import admin
from .models import MyModel

# Регистрация моделей для админ-панели.
admin.site.register(MyModel)
