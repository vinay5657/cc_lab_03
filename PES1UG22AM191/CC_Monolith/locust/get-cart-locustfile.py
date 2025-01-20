from locust import task, FastHttpUser
from insert_product import login

class CartTest(FastHttpUser):
    host = "http://localhost:5000"
    username = "test123"
    password = "test123"

    # Consolidating headers at the class level
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Upgrade-Insecure-Requests": "1"
    }

    def on_start(self):
        # Perform login and store the token
        cookies = login(self.username, self.password)
        self.token = cookies.get("token")

    @task
    def view_cart(self):
        headers = {**self.default_headers, "Cookies": f"token={self.token}"}

        # Use `get` to minimize overhead for simple GET requests
        with self.client.get("/cart", headers=headers, catch_response=True) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Failed to load cart: {resp.status_code}")
