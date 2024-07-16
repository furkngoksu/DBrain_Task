from kafka import KafkaProducer
import requests
from bs4 import BeautifulSoup
import json
import time

# This function will wait for Kafka to be ready before returning a producer
def wait_for_kafka():
    retries = 10
    for i in range(retries):
        try:
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("Connected to Kafka")
            return producer
        except Exception as e:
            print(f"Kafka not ready, retrying in 5 seconds... ({i+1}/{retries})")
            time.sleep(5)
    raise Exception("Could not connect to Kafka")

producer = wait_for_kafka()

BASE_URL = "https://scrapeme.live/shop/"

# This function will scrape the product names from the website
def get_product_names():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('h2', class_='woocommerce-loop-product__title')
    return [product.text for product in products]

# This function will scrape the product data from the website
def get_product_data(product_name):
    product_url = BASE_URL + product_name.replace(" ", "-")
    response = requests.get(product_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    name = soup.find('h1', class_='product_title').text
    
    price_container = soup.find('p', class_='price')
    price = price_container.find('span', class_='woocommerce-Price-amount').text.strip() if price_container else "N/A"
        
    description = soup.find('div', class_='woocommerce-product-details__short-description').text.strip() if soup.find('div', class_='woocommerce-product-details__short-description') else "No description"
    stock = soup.find('p', class_='stock').text.strip() if soup.find('p', class_='stock') else "In stock"
    
    return {
        "name": name,
        "price": price,
        "description": description,
        "stock": stock
    }


while True:
    product_names = get_product_names()
    if not product_names:
        print("No products found!")
        producer.send('test-topic', {"message": "No products found!"})
    else:
        for name in product_names:
            product_data = get_product_data(name)
            print(f"Sent: {product_data}")
            producer.send('test-topic', product_data)
    time.sleep(1)
    
