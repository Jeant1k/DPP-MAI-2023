from django.shortcuts import render

# Пример функции-представления.
def index(request):
    return render(request, 'index.html')
