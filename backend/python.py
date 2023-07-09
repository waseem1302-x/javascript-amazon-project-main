import os
import requests
from bs4 import BeautifulSoup
import random
import json
import string

# URL of the webpage
url = "http://127.0.0.1:5500/amazon.html"

# Send a GET request to the webpage
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find all product containers
product_containers = soup.find_all("div", class_="product-container")

# Create a list to store the extracted data
product_data = []

# Initialize a counter for product IDs
product_id_counter = 1

# Define a list of colors for product labels
colors = ["red", "blue", "green", "yellow", "orange", "purple"]

# Define a list of shipping locations
shipping_locations = ["USA", "UK", "Canada", "Australia", "Germany", "France", "Japan", "India", "Brazil", "Mexico"]

# Define a dictionary mapping product types to keywords
type_keywords = {
    "socks": ["athletic", "cotton", "socks"],
    "basketball": ["intermediate", "composite", "basketball"],
    "t-shirt": ["adults", "plain", "cotton", "t-shirt"],
}

# Define a dictionary mapping product types to categories
type_categories = {
    "socks": "Fashion",
    "basketball": "Sports & Outdoors",
    "t-shirt": "Fashion",
}

# Define a list of product descriptions
product_descriptions = [
    "High-quality material and comfortable fit.",
    "Durable and long-lasting design.",
    "Perfect for everyday use.",
    "Enhance your performance with this top-rated product.",
    "Versatile and stylish.",
    "An essential item for any wardrobe.",
]

# Iterate over each product container
for container in product_containers:
    try:
        # Extract the image URL
        image = container.find("img", class_="product-image")["src"]
        
        # Extract the product name
        name_element = container.find("div", class_="product-name")
        name = name_element.text.strip() if name_element else ""
        
        # Extract the product rating
        rating = container.find("div", class_="product-rating-count").text.strip()
        
        # Assign a unique ID to the product
        product_id = f"product_{product_id_counter}"
        product_id_counter += 1
        
        # Extract the product price
        price = container.find("div", class_="product-price").text.strip()
        
        # Determine the product type based on the name
        product_type = None
        for type_name, keywords in type_keywords.items():
            if all(keyword.lower() in name.lower() for keyword in keywords):
                product_type = type_name
                break
        
        # If the product type is found, use its keywords; otherwise, use an empty list
        keywords = type_keywords.get(product_type, [])
        
        # Generate a random discount percentage
        discount_percentage = random.randint(10, 50)
        
        # Calculate the discounted price
        price_cents = float(price[1:]) * 100  # Convert the price to cents
        discounted_price_cents = price_cents * (100 - discount_percentage) / 100
        
        # Generate a random product description
        description = random.choice(product_descriptions)
        
        # Generate a random customer rating
        customer_rating = round(random.uniform(3.5, 5.0), 1)
        
        # Generate a random SKU (stock keeping unit)
        sku = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        # Generate a random color for the product label
        color = random.choice(colors)
        
        # Generate a random shipping location
        shipping_location = random.choice(shipping_locations)
        
        # Generate a random product category
        category = type_categories.get(product_type, "Other")
        
        # Create a dictionary to store the product data
        product = {
            "id": product_id,
            "image": image,
            "name": name,
            "rating": rating,
            "price": price,
            "discount_percentage": discount_percentage,
            "discounted_price_cents": discounted_price_cents,
            "keywords": keywords,
            "description": description,
            "customer_rating": customer_rating,
            "sku": sku,
            "color": color,
            "shipping_location": shipping_location,
            "category": category
        }
        
        # Append the product data to the list
        product_data.append(product)
    except Exception as e:
        print(f"An error occurred while processing a product container: {e}")

# Create the directory to save the JSON file
directory = "backend"
os.makedirs(directory, exist_ok=True)

# Specify the path to save the JSON file
file_path = os.path.join(directory, "product_data.json")

# Save the product data as JSON
with open(file_path, "w") as file:
    json.dump(product_data, file, indent=4)

# Print the path where the JSON file is saved
print(f"Product data saved as JSON at: {file_path}")
