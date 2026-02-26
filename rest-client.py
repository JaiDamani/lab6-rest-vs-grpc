#!/usr/bin/env python3
from __future__ import print_function
import requests
import json
import time
import sys
import base64
import jsonpickle
import random

def doRawImage(addr, debug=False, session=None):
    # prepare headers for http request
    headers = {'content-type': 'image/png'}
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    # send http request with image and receive response
    image_url = addr + '/api/rawimage'
    if session:
        response = session.post(image_url, data=img, headers=headers)
    else:
        response = requests.post(image_url, data=img, headers=headers)
    if debug:
        # decode response
        print("Response is", response)
        print(json.loads(response.text))

def doAdd(addr, debug=False, session=None):
    headers = {'content-type': 'application/json'}
    # send http request with image and receive response
    add_url = addr + "/api/add/5/10"
    if session:
        response = session.post(add_url, headers=headers)
    else:
        response = requests.post(add_url, headers=headers)
    if debug:
        # decode response
        print("Response is", response)
        print(json.loads(response.text))

def doDotProduct(addr, debug=False, session=None):
    headers = {'content-type': 'application/json'}
    url = addr + '/api/dotproduct'
    a = [random.random() for _ in range(100)]
    b = [random.random() for _ in range(100)]
    payload = {'a': a, 'b': b}
    if session:
        response = session.post(url, json=payload, headers=headers)
    else:
        response = requests.post(url, json=payload, headers=headers)
    if debug:
        print("Response is", response)
        print(json.loads(response.text))

def doJsonImage(addr, debug=False, session=None):
    headers = {'content-type': 'application/json'}
    url = addr + '/api/jsonimage'
    img_bytes = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    img_b64 = base64.b64encode(img_bytes).decode('utf-8')
    payload = {'image': img_b64}
    if session:
        response = session.post(url, json=payload, headers=headers)
    else:
        response = requests.post(url, json=payload, headers=headers)
    if debug:
        print("Response is", response)
        print(json.loads(response.text))

if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} <server ip> <cmd> <reps>")
    print(f"where <cmd> is one of add, rawImage, sum or jsonImage")
    print(f"and <reps> is the integer number of repititions for measurement")

host = sys.argv[1]
cmd = sys.argv[2]
reps = int(sys.argv[3])

addr = f"http://{host}:5000"
print(f"Running {reps} reps against {addr}")

if cmd == 'rawImage':
    start = time.perf_counter()
    session = requests.Session()
    for x in range(reps):
        doRawImage(addr, session=session)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
elif cmd == 'add':
    start = time.perf_counter()
    session = requests.Session()
    for x in range(reps):
        doAdd(addr, session=session)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
elif cmd == 'jsonImage':
    start = time.perf_counter()
    session = requests.Session()
    for x in range(reps):
        doJsonImage(addr, debug=True if reps == 1 else False, session=session)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
elif cmd == 'dotProduct':
    start = time.perf_counter()
    session = requests.Session()
    for x in range(reps):
        doDotProduct(addr, debug=True if reps == 1 else False, session=session)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
else:
    print("Unknown option", cmd)