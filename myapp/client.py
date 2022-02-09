import random
import sys
import time

import grpc

from .calculator_pb2_grpc import CalculatorStub
from .calculator_pb2 import Operation


def grpc_query():
    with grpc.insecure_channel('server:50051') as channel:
        stub = CalculatorStub(channel)
        req = Operation(
            lhs=random.randrange(0, 1000),
            rhs=random.randrange(0, 1000),
            op=random.choice([Operation.ADD, Operation.SUB, Operation.MUL, Operation.DIV, Operation.MOD])
        )
        print(f'Sending request: {req}')
        res = stub.Calculate(req)
        print(f'Response: {res}')


def main():
    while True:
        try:
            grpc_query()
        except Exception as exc:
            sys.stderr.write(f'Exception raised: {exc}, continue')
        time.sleep(3)
