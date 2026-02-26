import grpc
from concurrent import futures
import time

import lab6_pb2
import lab6_pb2_grpc
from PIL import Image
import io
import base64

class Lab6Servicer(lab6_pb2_grpc.Lab6Servicer):
    def add(self, request, context):
        return lab6_pb2.addReply(sum=request.a + request.b)

    def rawImage(self, request, context):
        try:
            ioBuffer = io.BytesIO(request.img)
            img = Image.open(ioBuffer)
            return lab6_pb2.imageReply(width=img.size[0], height=img.size[1])
        except Exception as e:
            return lab6_pb2.imageReply(width=0, height=0)

    def dotProduct(self, request, context):
        try:
            dp = sum([x * y for x, y in zip(request.a, request.b)])
            return lab6_pb2.dotProductReply(dotproduct=dp)
        except Exception as e:
            return lab6_pb2.dotProductReply(dotproduct=0.0)

    def jsonImage(self, request, context):
        try:
            img_bytes = base64.b64decode(request.img)
            ioBuffer = io.BytesIO(img_bytes)
            img = Image.open(ioBuffer)
            return lab6_pb2.imageReply(width=img.size[0], height=img.size[1])
        except Exception as e:
            return lab6_pb2.imageReply(width=0, height=0)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lab6_pb2_grpc.add_Lab6Servicer_to_server(Lab6Servicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
