import random, os
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
        self.client.post("%s/api/post" % host, {
            'message': 'hello world'
        }, name="/api/post (flask)")

    # Java Spring
    @tag('spring_auto')
    @task
    def spring_root(self):
        host = 'http://' + os.environ.get('SPRING_HOST', 'localhost:8080')
        name = random.choice(table_key_names)
        self.client.get("%s/" % host, name="/ (spring)")

    @tag('spring_auto')
    @task(3)
    def spring_demo(self):
        host = 'http://' + os.environ.get('SPRING_HOST', 'localhost:8080')
        spring_status = random.choice(spring_statuses)
        self.client.get("%s/api/demo" % host, params={"status": spring_status}, name="/api/demo")

    @tag('spring_auto')
    @task
    def spring_flask(self):
        host = 'http://' + os.environ.get('SPRING_HOST', 'localhost:8080')
        name = random.choice(table_key_names)
        self.client.get("%s/api/flask" % host, params={"name": name}, name="/api/lambda")

    @tag('spring_auto')
    @task
    def spring_post(self):
        host = 'http://' + os.environ.get('SPRING_HOST', 'localhost:8080')
        self.client.post("%s/api/post" % host, {
            'message': 'hello world'
        }, name="/api/post (spring)")

