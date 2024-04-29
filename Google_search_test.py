from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
import time

def setup_driver():
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)
    return driver

def connect_database():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='IcandoIt@2024',
        database='MY_CUSTOM_BOT'
    )
    return conn

def save_search_results(cursor, search_term_id, url, frequency=1):
    try:
        query = """
        INSERT INTO searchresults (SearchTermID, URL, Frequency)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE Frequency = Frequency + 1;
        """
        cursor.execute(query, (search_term_id, url,  frequency))
    except mysql.connector.Error as err:
        print("Error inserting data:", err)

def get_search_engine():
    engines = {
        'google': "https://www.google.com/",
        'bing': "https://www.bing.com/",
        'yahoo': "https://search.yahoo.com/",
        'duckduckgo': "https://duckduckgo.com/"
    }
    while True:
        search_engine = input("Enter the search engine (google, bing, yahoo, duckduckgo): ").lower()
        if search_engine in engines:
            return search_engine
        else:
            print("Invalid search engine. Please choose from google or bing.")

def search_and_capture(conn, search_term_id, term, search_engine):
    engines = {
        'google': "https://www.google.com/",
        'bing': "https://www.bing.com/",
        'yahoo': "https://search.yahoo.com/",
        'duckduckgo': "https://duckduckgo.com/"
    }

    driver = setup_driver()
    driver.get(engines[search_engine])

    search_box_name = 'q'
    input_element = driver.find_element(By.NAME, search_box_name)
    input_element.send_keys(term)
    input_element.send_keys(Keys.RETURN)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h3')))

    search_results = driver.find_elements(By.CSS_SELECTOR, 'a > h3')
    cursor = conn.cursor()
    for result in search_results:
        url = result.find_element(By.XPATH, '..').get_attribute('href')
        if url:  
            save_search_results(cursor, search_term_id, url)
    
    conn.commit()
    cursor.close()
    driver.quit()

def display_results(conn, limit=100):
    query = """
    SELECT URL, Frequency FROM searchresults
    ORDER BY Frequency DESC
    LIMIT %s;
    """
    cursor = conn.cursor()
    cursor.execute(query, (limit,))
    results = cursor.fetchall()
    for url, frequency in results:
        print(f"URL: {url}, Frequency: {frequency}")
    cursor.close()

def main():
    conn = connect_database()
    if conn is None:
        print("Failed to connect to database.")
        return

    search_engine = get_search_engine()
    search_term_id = 1  
    search_term = input("Enter Search Query: ")
    search_and_capture(conn, search_term_id, search_term, search_engine)
    
    # Display results after capturing them
    display_results(conn, 100)

    conn.close()

if __name__ == "__main__":
    main()
