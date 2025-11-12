import requests

BASE_URL = "http://localhost:5000/items"

def list_items():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        items = response.json()
        print("Items:", items)
    else:
        print("Error:", response.json())

def create_item(name, description=""):
    payload = {"name": name, "description": description}
    response = requests.post(BASE_URL, json=payload)
    if response.status_code == 201:
        print("Item created:", response.json())
    else:
        print("Error:", response.json())

def get_item(item_id):
    response = requests.get(f"{BASE_URL}/{item_id}")
    if response.status_code == 200:
        item = response.json()
        print("Item:", item)
    else:
        print("Error:", response.json())

def update_item(item_id, name=None, description=None):
    payload = {}
    if name:
        payload["name"] = name
    if description:
        payload["description"] = description
    response = requests.put(f"{BASE_URL}/{item_id}", json=payload)
    if response.status_code == 200:
        print("Item updated:", response.json())
    else:
        print("Error:", response.json())

def delete_item(item_id):
    response = requests.delete(f"{BASE_URL}/{item_id}")
    if response.status_code == 204:
        print("Item deleted")
    else:
        print("Error:", response.json())

if __name__ == "__main__":
    # Example usage
    list_items()
    create_item("Sample Item", "This is a sample item.")
    #get_item(1)
    #update_item(1, description="Updated description.")
    #delete_item(1)