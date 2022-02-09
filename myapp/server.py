from concurrent import futures

import grpc

from .calculator_pb2_grpc import add_CalculatorServicer_to_server, CalculatorServicer
from .calculator_pb2 import Operation, Result


class MyCalculator(CalculatorServicer):
    def Calculate(self, request, context):
        print(f'Got call, request={request}')

        ops = {
            Operation.ADD: lambda a, b: a + b,
            Operation.SUB: lambda a, b: a - b,
            Operation.MUL: lambda a, b: a * b,
            Operation.DIV: lambda a, b: a // b,
            Operation.MOD: lambda a, b: a % b,
        }

        result = ops[request.op or Operation.ADD](request.lhs, request.rhs)
        resp = Result(value=result)

        print(f'Return: {resp}')
        return resp


def main():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
  add_CalculatorServicer_to_server(
      MyCalculator(), server
  )
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()
