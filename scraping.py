from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
from google.cloud import bigquery
import pandas as pd
from tempfile import NamedTemporaryFile

# Set the environment variable to authenticate with Google Cloud
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/app/challenge-borda-80fb1feb52cb.json'

# Create a BigQuery client
client = bigquery.Client()

# Configure Chrome options to run it in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--no-sandbox")  # Disable sandboxing
chrome_options.add_argument("--disable-dev-shm-usage")  # Use /dev/shm for shared memory
chrome_options.add_argument("--disable-gpu")  # Disable the GPU
chrome_options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging port
chrome_options.add_argument("--disable-extensions")  # Disable Chrome extensions

# Set up the browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open the Yogonet page
driver.get("https://www.yogonet.com/international/")

try:
    # Wait until the article container is present and interactive to click
    article = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "body > div.contenedor_general_estructura.estructura_home.publicidad_mobile_ubicada.fin_carga > div:nth-child(6) > div > div.slot.slot_1.noticia.cargada > div > div.volanta_titulo")
        )
    )
    article.click()
    print("Article clicked successfully.")
    
    # Wait for the title container to load on the new page
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "body > div.contenedor_general_estructura.estructura_news.publicidad_mobile_ubicada.fin_carga > div.contenedor_modulo.contenido_de_noticia > div > div.slot.contenido_fijo.titulo_de_noticia > h1")
        )
    )

    # Get the current page link after clicking
    article_link = driver.current_url
    
    # Find the title
    title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "body > div.contenedor_general_estructura.estructura_news.publicidad_mobile_ubicada.fin_carga > div.contenedor_modulo.contenido_de_noticia > div > div.slot.contenido_fijo.titulo_de_noticia > h1")
        )
    ).text
    
    # Find the kicker
    kicker = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "body > div.contenedor_general_estructura.estructura_news.publicidad_mobile_ubicada.fin_carga > div.contenedor_modulo.contenido_de_noticia > div > div.slot.contenido_fijo.titulo_de_noticia > div.volanta_noticia.fuente_roboto_slab")
        )
    ).text
    
    # Find the image
    image = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "body > div.contenedor_general_estructura.estructura_news.publicidad_mobile_ubicada.fin_carga > div.contenedor_modulo.contenido_de_noticia > div > div.slot.contenido_fijo.imagen_noticia > img")
        )
    ).get_attribute('src')
    
    # Perform post-processing
    word_count = len(title.split())
    char_count = len(title)
    capitalized_words = ', '.join([word for word in title.split() if word.istitle()])

    # Prepare the data to insert into BigQuery
    data = [
        {
            'title': title,
            'kicker': kicker,
            'image': image,
            'link': article_link,
            'word_count': word_count,
            'char_count': char_count,
            'capitalized_words': capitalized_words
        }
    ]
    
    # Set up the DataFrame
    df = pd.DataFrame(data)

    # Save the DataFrame to a temporary CSV file
    with NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8') as temp_file:
        df.to_csv(temp_file.name, index=False)

    # Define the Dataset and Table
    dataset_id = 'challenge_dataset'
    table_id = 'table_scraping'
    table_ref = client.dataset(dataset_id).table(table_id)

    # Configure data load without schema autodetection
    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("title", "STRING"),
            bigquery.SchemaField("kicker", "STRING"),
            bigquery.SchemaField("image", "STRING"),
            bigquery.SchemaField("link", "STRING"),
            bigquery.SchemaField("word_count", "INTEGER"),
            bigquery.SchemaField("char_count", "INTEGER"),
            bigquery.SchemaField("capitalized_words", "STRING")
        ],
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1
    )

    # Load the data into BigQuery using batch loading
    with open(temp_file.name, 'rb') as source_file:
        load_job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

    # Wait for the job to complete
    load_job.result()

    print("Data loaded successfully into BigQuery.")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the browser
    driver.quit()
