import random, os, json
from locust import HttpUser, TaskSet, between, task, tag

table_key_names = [
    'apple',
    'orange',
    'banana',
    'strawberry',
    'error'
    ]

lambda_types = [
    'proxy',
    'non-proxy',
    'other'
    ]

spring_statuses = [
    'success',
    'error',
    'other'
    ]

gorilla_httpstatus = [
    '200',
    '302',
    '404',
    '418',
    '500',
    '502'
]


class RestUser(HttpUser):
    wait_time = between(5, 15)
    host = 'http://localhost'
    
    def on_start(self):
        print('**Start Load Generator by Locust**')
    
    def on_stop(self):
        print('**Stop Load Generator by Locust**')

    # Python Flask
    @tag('flask_auto')
    @task(3)
    def flask_root(self):
        host = 'http://' + os.environ.get('FLASK_HOST', 'localhost:5050')
        name = random.choice(table_key_names)
        self.client.get(f"{host}/?name={name}", name="/ (flask)")

    @tag('flask_auto')
    @task(3)
    def flask_lambda(self):
        host = 'http://' + os.environ.get('FLASK_HOST', 'localhost:5050')
        lambda_type = random.choice(lambda_types)
        self.client.get("%s/api/lambda" % host, params={"type": lambda_type}, name="/api/lambda")

    @tag('flask_auto')
    @task
    def flask_lambda_jaeger(self):
        host = 'http://' + os.environ.get('FLASK_HOST', 'localhost:5050')
        self.client.get("%s/api/lambda/jaeger" % host)

    @tag('flask_auto')
    @task(3)
    def flask_spring(self):
        host = 'http://' + os.environ.get('FLASK_HOST', 'localhost:5050')
        spring_status = random.choice(spring_statuses)
        self.client.get("%s/api/spring" % host, params={"status": spring_status}, name="/api/spring")

    @tag('flask_auto')
    @task
    def flask_post(self):
        host = 'http://' + os.environ.get('FLASK_HOST', 'localhost:5050')
        self.client.post("%s/api/post" % host, data=json.dumps({
            'message': 'hello world'
        }), headers={
            'Content-Type': 'application/json'
        }, name="/api/post (flask)")

    # Java Spring
    @tag('spring_auto')
    @task
    def spring_root(self):
        host = 'http://' + os.environ.get('SPRING_HOST', 'localhost:8080')
        self.client.get("%s/" % host, name="/ (spring)")

    @tag('spring_auto')
    @task(3)
    def spring_demo(self):
        host = 'http://' + os.environ.get('SPRING_HOST', 'localhost:8080')
        spring_status = random.choice(spring_statuses)
        self.client.get("%s/api/demo" % host, params={"status": spring_status}, name="/api/demo")

    @tag('spring_auto')
    @task(5)
    def spring_flask(self):
        host = 'http://' + os.environ.get('SPRING_HOST', 'localhost:8080')
        name = random.choice(table_key_names)
        self.client.get("%s/api/flask" % host, params={"name": name}, name="/api/flask")

    @tag('spring_auto')
    @task
    def spring_post(self):
        host = 'http://' + os.environ.get('SPRING_HOST', 'localhost:8080')
        self.client.post("%s/api/post" % host, data=json.dumps({
            'message': 'hello world'
        }), headers={
            'Content-Type': 'application/json'
        }, name="/api/post (spring)")

    @tag('spring_auto')
    @task(6)
    def spring_gorilla_id(self):
        host = 'http://' + os.environ.get('SPRING_HOST', 'localhost:8080')
        httpstatus = random.choice(gorilla_httpstatus)
        self.client.get("%s/api/gorilla/id" % host, params={"httpStatus": httpstatus}, name="/api/gorilla/id")

    @tag('spring_auto')
    @task(3)
    def spring_postgresql(self):
        host = 'http://' + os.environ.get('SPRING_HOST', 'localhost:8080')
        name = random.choice(table_key_names)
        self.client.get("%s/api/postgresql" % host, params={"name": name}, name="/api/postgresql")

    # Go Gorilla
    @tag('gorilla_auto')
    @task
    def gorilla_root(self):
        host = 'http://' + os.environ.get('GORILLA_HOST', 'localhost:9090')
        self.client.get("%s/" % host, name="/ (gorilla/mux)")

    @tag('gorilla_auto')
    @task
    def gorilla_post(self):
        host = 'http://' + os.environ.get('GORILLA_HOST', 'localhost:9090')
        self.client.post("%s/api/post" % host, data=json.dumps({
            'message': 'hello world'
        }), headers={
            'Content-Type': 'application/json'
        }, name="/api/post (gorilla/mux)")

    @tag('gorilla_auto')
    @task
    def gorilla_grpc_list(self):
        host = 'http://' + os.environ.get('GORILLA_HOST', 'localhost:9090')
        self.client.get("%s/api/grpc/animal" % host, name="/api/grpc/animal (gorilla)")

    @tag('gorilla_auto')
    @task
    def gorilla_grpc_get(self):
        host = 'http://' + os.environ.get('GORILLA_HOST', 'localhost:9090')
        self.client.get("%s/api/grpc/animal/a27628d8-e3b3-4da3-98c7-0f33efc7f45f" % host)

    @tag('gorilla_auto')
    @task
    def gorilla_grpc_post_delete(self):
        host = 'http://' + os.environ.get('GORILLA_HOST', 'localhost:9090')
        r = self.client.post("%s/api/grpc/animal" % host, data=json.dumps({
            'type': 'locust', 
            'name': 'taro', 
            'height': 100, 
            'weight': 200, 
            'region': [
              'asia'
            ], 
            'isCattle': False
        }), headers={
            'Content-Type': 'application/json'
        }, name="/api/grpc/animal (gorilla)")
        dict_r = json.loads(r.text)
        animal_id = dict_r.get('id', '')
        self.client.get("%s/api/grpc/animal/%s" % (host, animal_id), name="/api/grpc/animal/{id:[0-9a-f-]+} (gorilla)")
        self.client.delete("%s/api/grpc/animal/%s" % (host, animal_id), name="/api/grpc/animal/{id:[0-9a-f-]+} (gorilla)")

    @tag('express_auto')
    @task
    def express_gorilla_animal(self):
        host = 'http://' + os.environ.get('EXPRESS_HOST', 'localhost:3030')
        self.client.get("%s/api/gorilla/animal" % host, name="/api/gorilla/animal (Node.js)")

    @tag('express_auto')
    @task
    def express_grpc_list(self):
        host = 'http://' + os.environ.get('EXPRESS_HOST', 'localhost:3030')
        self.client.get("%s/api/grpc/animal" % host, name="/api/grpc/animal (express)")

    @tag('express_auto')
    @task
    def express_grpc_post_delete(self):
        host = 'http://' + os.environ.get('EXPRESS_HOST', 'localhost:3030')
        r = self.client.post("%s/api/grpc/animal" % host, data=json.dumps({
            'type': 'locust', 
            'name': 'taro', 
            'height': 100, 
            'weight': 200, 
            'region': [
              'asia'
            ], 
            'isCattle': False
        }), headers={
            'Content-Type': 'application/json'
        }, name="/api/grpc/animal (express)")
        dict_r = json.loads(r.text)
        animal_id = dict_r.get('id', '')
        self.client.get("%s/api/grpc/animal/%s" % (host, animal_id), name="/api/grpc/animal/{id:[0-9a-f-]+} (express)")
        self.client.delete("%s/api/grpc/animal/%s" % (host, animal_id), name="/api/grpc/animal/{id:[0-9a-f-]+} (express)")

    @tag('type_express_auto')
    @task
    def type_express_gorilla_animal(self):
        host = 'http://' + os.environ.get('TYPE_EXPRESS_HOST', 'localhost:3031')
        self.client.get("%s/api/gorilla/animal" % host, name="/api/gorilla/animal (TypeScript)")
