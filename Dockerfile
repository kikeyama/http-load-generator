FROM python:3
ADD locustfile.py /
ADD requirements.txt /
# ENV FLASK_HOST <FLASK_HOST>    # localhost:5050
# ENV SPRING_HOST <FLASK_HOST>    # localhost:8080
RUN pip install -r requirements.txt
#CMD [ "locust", "locustfile.py", "RestUser", "--headless", "-u", "100", "-r", "10" ]
CMD locust -f locustfile.py RestUser --headless -u 30 -r 20
