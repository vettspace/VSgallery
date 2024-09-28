# VSgallery 
```(in progress...)```

## Описание

Небольшой. Личный. Амбициозный.
Здесь я по мере возможностей разрабатываю свой пет-проект. Его задача - дать 
фотографам удобный инструмент, чтобы делиться отснятыми материалами с 
клиентами. Главная цель - простота, скорость, элегантность инструмента.



## Установка

Чтобы развернуть проект на локальной машине, выполните следующие шаги:

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/vettspace/VSgallery.git
   cd photo_gallery
   ```

2. **Создайте и активируйте виртуальное окружение:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Для Linux/MacOS
   venv\Scripts\activate  # Для Windows
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Примените миграции:**
   ```bash
   python manage.py migrate
   ```

5. **Запустите сервер разработки:**
   ```bash
   python manage.py runserver
   ```
