This project implements a simple GRPC server and client in Python. The goal is to explain the basics of GRPC for people who never read any documentation about it and would like to understand a few core concepts.

# Usage

```
$> make up
```

This command generates Python files from [calculator.proto](myapp/calculator.proto), and starts two containers. The server container listens for connection and exposes a service to perform arithmetical operations. The client container attempts to connect to the server every few seconds and calls this service.

# How does it work

## Service file

[calculator.proto](myapp/calculator.proto) contains the gRPC service definition.

To define a structure `Result` with an int32 field `value`:

```
message Operation {
    int32 lhs = 1;
    int32 rhs = 2;

    enum OperationType {
        ADD = 0;
        SUB = 1;
        MUL = 2;
        DIV = 3;
        MOD = 4;
    }

    optional OperationType op = 3;
}
```

To define a service:

```
service Calculator {
    rpc Calculate(Operation) returns (Result);
}
```

Here the service is a simple RPC, but three other kinds of services exist:

* response-streaming RPC
* request-streaming RPC
* bidirectionally-streaming RPC

> The " = 1", " = 2" markers on each element identify the unique "tag" that field uses in the binary encoding.

See also: https://developers.google.com/protocol-buffers/docs/pythontutorial

## Code generation

[Makefile](Makefile) has a rule `proto` which calls `python -m grpc_tools.protoc` to generate [myapp/calculator_pb2.py](myapp/calculator_pb2.py) and [myapp/calculator_pb2_grpc.py](myapp/calculator_pb2_grpc.py).

* *calculator_pb2.py* contains classes for the messages defined in the proto file.
* *calculator_pb2_grpc.py* defines the interfaces for server implementation.

## Server

Server implementation is in [myapp/server.py](myapp/server.py).

`MyCalculator` inherits `CalculatorServicer` and contains the function `Calculate` which is the implementation of our RPC.

The function takes two parameters. `request` is an object of type `Operation`, with attributes `lhs`, `rhs` and `op`. The second parameter is the [GRPC context](https://grpc.github.io/grpc-java/javadoc/io/grpc/Context.html).

> A context propagation mechanism which can carry scoped-values across API boundaries and between threads. Examples of state propagated via context include:
> * Security principals and credentials.
> * Local and distributed tracing information.


## Client

Client implementation is in [myapp/client.py](myapp/client.py).

In GRPC terminology, a *channel* is a connection to a gRPC server, and a *stub* is a client which can be synchronous (for simple RPC) or asynchronous (for streaming RPC).

To create a gRPC client, you first create a channel:

```python
with grpc.insecure_channel('server:50051') as channel:
```

Then you create a stub:

```python
    stub = CalculatorStub(channel)
```

and you can perform the RPC:

```python
    req = Operation(
        lhs=10,
        rhs=20,
        op=Operation.ADD
    )
    res = stub.Calculate(req)
```
