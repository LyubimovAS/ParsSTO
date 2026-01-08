import time
import re
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from database import get_db_connection, init_db  # твои функции для работы с БД

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Функция для очистки цены
def clean_price(price_str):
    if not price_str:
        return 0
    digits = re.sub(r'\D', '', price_str)
    return int(digits) if digits else 0

def run_parser():
    # Инициализация БД
    init_db()
    
    url = "https://oiler.pro/ua-ua/sto/sto-obolon/"
    
    # Настройка Selenium
    options = Options()
    options.add_argument("--start-maximized")  # окно открывается большое
    # options.add_argument("--headless")  # закомментируй, чтобы видеть браузер
    
    logging.info("Запускаю браузер...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        logging.info("Сайт открыт, жду 3 секунды...")
        time.sleep(3)

        # Скроллим страницу вниз, чтобы все аккордеоны подгрузились
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        laters = ['1', '2', '3']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM repair_services")  # очищаем таблицу
        conn.commit()
        for numb in laters:
            # Получаем все контейнеры аккордеонов
            items = driver.find_elements(By.CSS_SELECTOR, f'div.lig{numb}[role="tablist"]')


            
            logging.info(f"Найдено {len(items)} категорий услуг.")
            
            total_records = 0
            print(items)
            for item in items:
                try:
                    # Кликаем по кнопке аккордеона
                    button = item.find_element(By.CSS_SELECTOR, 'div[data-role="trigger"]')
                    driver.execute_script("arguments[0].click();", button)
                    time.sleep(1)  # ждем загрузки контента

                    category = button.text.strip()
                    # logging.info(f"Категория: {category}")

                    # Берем все услуги внутри аккордеона
                    services = item.find_elements(By.CSS_SELECTOR, 'div.accordion-subitem__wraper')
                    for s in services:
                        try:
                            name_el = s.find_element(By.CSS_SELECTOR, 'div.subitem-title')
                            price_el = s.find_element(By.CSS_SELECTOR, 'div.subitem-price')
                            service_name = name_el.text.strip()
                            price_raw = clean_price(price_el.text.strip())

                            # logging.info(f"Услуга: {service_name}, Цена: {price}")

                            # Сохраняем в БД
                            cursor.execute(
                                "INSERT INTO repair_services (category, service_name, price_raw) VALUES (?, ?, ?)",
                                (category, service_name, price_raw)
                            )
                            total_records += 1
                        except Exception as e:
                            logging.warning(f"Ошибка при обработке услуги: {e}")
                    
                    conn.commit()
                except Exception as e:
                    logging.warning(f"Ошибка при обработке категории: {e}")

            logging.info(f"Успех! В базу добавлено: {total_records} записей.")

    finally:
        driver.quit()
        conn.close()
        logging.info("Парсер завершил работу.")

if __name__ == "__main__":
    run_parser()
