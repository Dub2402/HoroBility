# HoroBility
**HoroBility** – [Telegram](https://telegram.org)-бот, помогающий узнать общую совместимость знаков зодиака, и совместимость на сегодняшний день.

## Порядок установки и использования

1. Для установки необходимо наличие системы [Git](https://git-scm.com/downloads).
2. Установить [Python](https://www.python.org/downloads/) версии 3.11 или выше. Рекомендуется добавить в PATH.


3. Клонируйте репозиторий рекурсивно (для автоматического включения подмодулей).

```git clone https://github.com/Dub2402/HoroBility --recursive```

4. Открыть каталог со скриптом в консоли: можно воспользоваться командой cd или встроенными возможностями файлового менеджера.

5. Создать виртуальное окружение Python.

```
python -m venv .venv
```

6. Активировать вирутальное окружение.

#### Для Windows.
    
```shell
.venv\Scripts\activate.bat
```

#### Для Linux или MacOS.

```bash
source .venv/bin/activate
```

7. Установить зависимости скрипта.

```
pip install -r requirements.txt
```

8. Настроить бота путём редактирования _Settings.json_.

### Settings.json.

```JSON
"token": ""
```

Указывается строковый токен бота Telegram (можно получить у [BotFather](https://t.me/BotFather)).

```JSON
"updating_time": "00:01"
```

Время ежедневного обновления файла _Response.json_ c данными совместимости знаков зодиака на сегодняшний день.

```JSON
"mailing_time": "07:01"
```

Время ежедневной рассылки гороскопа совместимости знаков зодиака на сегодняшний день.

```JSON
"share_image_path": ""
```

Путь к фото, которое присылается пользователю при нажатии кнопки "Поделиться с друзьями". Также присылается при первом запуске скрипта/изменении изображения, пользователю, чей ID указан в следующем пункте.

```JSON
"chat_id": null
```

Вводится ID пользователя Telegram в числовом формате (можно узнать у Chat ID Bot). Необходим для получения unique_id изображения, используемого для мгновенной отправки. 

```JSON
"password": null
```

Пароль для входа в административную панель.

9. Добавить текст на каждый ключ в файле **Совместимость.json** общую совместимость в виде текста html.

10. Добавить изображения, используемые в боте в папку Materials, со структурой показанной ниже.
<details>
<summary>Структура файлов<p></p></summary> 

```html

.
└── Materials/
    ├── Близнецы/
    │   ├── Близнецы.jpg 
    │   ├── Весы.jpg      <!-- Изображение, где первый знак близнецы, второй - весы. -->
    │   ├── Водолей.jpg
    │   ├── Дева.jpg
    │   ├── Козерог.jpg
    │   ├── Лев.jpg
    │   ├── Овен.jpg
    │   ├── Рак.jpg
    │   ├── Рыбы.jpg
    │   ├── Скорпион.jpg
    │   ├── Стрелец.jpg
    │   └── Телец.jpg
    ├── Весы/
    │   └── ...
    ├── Водолей
    ├── Дева
    ├── Козерог
    ├── Лев
    ├── Овен
    ├── Рак
    ├── Рыбы
    ├── Скорпион
    ├── Стрелец
    └── Телец

```
</details>

11. Запустить файл _main.py_.

```
python main.py
```

12. Для автоматического запуска рекомендуется провести инициализацию сервиса через [systemd](systemd/README.md) на Linux или путём добавления его в автозагрузку на Windows.

13. Перейти в чат с ботом, токен которого указан в настройках, и следовать его инструкциям.

---
**_Copyright © Dub Irina. 2024-2025._**
