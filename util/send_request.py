import requests
import json

def send_requests(data):

    obj = {"auth-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjU2NDJlN2M2N2NlMzE3NDEyNGMwNSIsImlhdCI6MTYxNTQ5Mjk4MCwiZXhwIjoxNjI1NDkyOTgwfQ.y9l01Fylk_lfwyym2dJ8z85m5F65KRQwmhoa16OwhyA"}

    url = "https://engo500.herokuapp.com/room/6068ef9e4938d400042f82db"

    session = requests.Session()
    r = session.put(url,headers=obj,json=data)
    print(r)