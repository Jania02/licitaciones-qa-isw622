import os
from locust import HttpUser, task, constant_pacing

class UsuarioQA(HttpUser):
    wait_time=constant_pacing(1)
    def on_start(self):
        with self.client.post('/api/auth/login',json={'username':os.environ['ADMIN_USER'],'password':os.environ['ADMIN_PASSWORD']},catch_response=True,name='login') as r:
            if r.status_code != 200: r.failure('Login sintético falló')
    @task
    def listar(self):
        self.client.get('/api/licitaciones',name='GET listado')
