import grpc
import time
import sys
import random
import base64

import lab6_pb2
import lab6_pb2_grpc

def doAdd(stub, debug=False):
    response = stub.add(lab6_pb2.addMsg(a=5, b=10))
    if debug:
        print("Response sum:", response.sum)

def doRawImage(stub, debug=False):
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    response = stub.rawImage(lab6_pb2.rawImageMsg(img=img))
    if debug:
        print(f"Response dimensions: {response.width}x{response.height}")

def doDotProduct(stub, debug=False):
    a = [random.random() for _ in range(100)]
    b = [random.random() for _ in range(100)]
    response = stub.dotProduct(lab6_pb2.dotProductMsg(a=a, b=b))
    if debug:
        print("Response dotproduct:", response.dotproduct)

def doJsonImage(stub, debug=False):
    img_bytes = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    img_b64 = base64.b64encode(img_bytes).decode('utf-8')
    response = stub.jsonImage(lab6_pb2.jsonImageMsg(img=img_b64))
    if debug:
        print(f"Response dimensions: {response.width}x{response.height}")

if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} <server ip> <cmd> <reps>")
    print(f"where <cmd> is one of add, rawImage, dotProduct, jsonImage")
    print(f"and <reps> is the integer number of repititions for measurement")
    sys.exit(1)

host = sys.argv[1]
cmd = sys.argv[2]
reps = int(sys.argv[3])

addr = f"{host}:50051"
print(f"Running {reps} reps against {addr}")

channel = grpc.insecure_channel(addr)
stub = lab6_pb2_grpc.Lab6Stub(channel)

if cmd == 'add':
    start = time.perf_counter()
    for x in range(reps):
        doAdd(stub, debug=True if reps == 1 else False)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
elif cmd == 'rawImage':
    start = time.perf_counter()
    for x in range(reps):
        doRawImage(stub, debug=True if reps == 1 else False)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
elif cmd == 'dotProduct':
    start = time.perf_counter()
    for x in range(reps):
        doDotProduct(stub, debug=True if reps == 1 else False)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
elif cmd == 'jsonImage':
    start = time.perf_counter()
    for x in range(reps):
        doJsonImage(stub, debug=True if reps == 1 else False)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
else:
    print("Unknown option", cmd)
