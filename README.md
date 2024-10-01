# VSgallery 
```(in progress...)```

## Описание

Небольшой. Личный. Амбициозный.
Здесь я по мере возможностей разрабатываю свой пет-проект. Его задача - дать 
фотографам удобный инструмент, чтобы делиться отснятыми материалами с 
клиентами. Главная цель - простота, скорость, элегантность инструмента.

<img width="1416" src="https://github.com/user-attachments/assets/db82ddad-28fa-41fc-a27b-fe63d32dc935">

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

<img width="1416" src="https://github.com/user-attachments/assets/1992214b-4863-4330-9642-bc4349797353">
<img width="1416" src="https://github.com/user-attachments/assets/28cf9d1e-2a7b-446b-a7d2-450b480cfc6a">

