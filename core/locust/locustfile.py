from locust import HttpUser, task, between

# __________________________________________________________

class QuickstartUser(HttpUser):
    def on_start(self):
        response = self.client.post("/accounts/api/v1/jwt/create/", 
                         data={'email':'admin@gmail.com','password':'Aa123456@'}).json()
        
        self.client.headers = {"Authorization": f"Bearer {response.get('access',None)}"} 
        
    @task
    def get_post_list(self):
        self.client.get("/blog/api/v1/posts/")
        
    @task
    def get_category_list(self):
        self.client.get("/blog/api/v1/categories/")
# __________________________________________________________