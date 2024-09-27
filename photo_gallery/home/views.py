from django.shortcuts import render


def homepage_view(request):
    """Главная страница."""
    return render(request, 'home/index.html')
