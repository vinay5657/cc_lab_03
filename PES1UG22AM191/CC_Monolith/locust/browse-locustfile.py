from locust import task, FastHttpUser
from insert_product import login  # Assuming login is required for some reason

class BrowseTest(FastHttpUser):
    host = "http://localhost:5000"
    
    # Consolidating headers at the class level
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Upgrade-Insecure-Requests": "1"
    }

    def on_start(self):
        # If login is required for authentication, get the token here.
        cookies = login("test123", "test123")  # Only if login is needed
        self.token = cookies.get("token")

    @task
    def browse_page(self):
        headers = {**self.default_headers, "Cookies": f"token={self.token}"}  # If token is needed
        
        # Using self.client.get for optimized GET request
        with self.client.get("/browse", headers=headers, catch_response=True) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Failed to load browse page: {resp.status_code}")
