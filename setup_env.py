import subprocess
import sys
import os

def install_dependencies():
    """
    Проверяет наличие файла requirements.txt и устанавливает библиотеки.
    """
    requirements_file = "requirements.txt"
    
    # Список необходимых библиотек для нашего проекта
    dependencies = [
        "requests==2.31.0",
        "beautifulsoup4==4.12.2",
        "fastapi==0.104.1",
        "uvicorn==0.24.0.post1",
        "lxml==4.9.3",
        "selenium==4.15.2",
        "webdriver-manager==4.0.1"
    ]
    
    # Если файла нет, создадим его автоматически
    if not os.path.exists(requirements_file):
        print(f"Файл {requirements_file} не найден. Создаю...")
        with open(requirements_file, "w", encoding="utf-8") as f:
            for dep in dependencies:
                f.write(f"{dep}\n")

    print("Проверка и установка зависимостей...")
    try:
        # Установка через текущий интерпретатор Python (важно для venv)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        print("Все библиотеки успешно установлены.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при установке библиотек: {e}")
        sys.exit(1)

def prepare_environment():
    """
    Создает структуру папок и инициализирует базу данных.
    """
    # 1. Создаем папку для данных, если ее нет
    if not os.path.exists("data"):
        os.makedirs("data")
        print("Папка 'data' создана.")

    # 2. Инициализируем базу данных
    # Мы импортируем init_db здесь, чтобы избежать ошибок, если библиотеки еще не стоят
    try:
        from database import init_db
        init_db()
        print("База данных успешно проинициализирована.")
    except ImportError:
        print("Предупреждение: Файл database.py не найден. Сначала создайте его.")
    except Exception as e:
        print(f"Ошибка при инициализации БД: {e}")

if __name__ == "__main__":
    print("=== Car Repair Project Setup ===")
    
    # Шаг 1: Установка библиотек
    install_dependencies()
    
    # Шаг 2: Настройка папок и БД
    prepare_environment()
    
    print("=== Настройка завершена успешно ===")