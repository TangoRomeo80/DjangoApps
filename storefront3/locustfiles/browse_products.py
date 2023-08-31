from locust import HttpUser, task, between
from random import randint


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)  # Define wait time between requests

    # View all products
    @task(2)
    def view_products(self):
        collection_id = randint(2, 6)
        self.client.get(
            f'/store/products/?collection_id={collection_id}',
            name='/store/products/'
        )

    # View a single product details
    @task(4)
    def view_product(self):
        product_id = randint(1, 1000)
        self.client.get(
            f'/store/products/{product_id}/',
            name='/store/products/:id'
        )

    # Adding a product to cart
    @task(1)
    def add_to_cart(self):
        product_id = randint(1, 10)
        self.client.post(
            f'/store/carts/{self.cart_id}/items/',
            name='/store/carts/items/',
            json={'product_id': product_id, 'quantity': 1}
        )

    # cart id to be generated when user adds product to cart, so use lifecycle hook
    def on_start(self):
        respone = self.client.post(
            '/store/carts/',
        )
        result = respone.json()
        self.cart_id = result['id']

# Run the test
