
from __future__ import print_function
from concurrent import futures
import random
import time
import math
import logging
import json
import grpc
import example_pb2
import example_pb2_grpc
import example_resources



request_db = example_resources.read_example_database()
startingport_id = 50050 

# send request to server and get response back here
def msg_delivery_one(stub, send_request):
    get_request = stub.MsgDelivery(send_request)
    if not send_request.id:
        print("Server returned incomplete feature")
        return None

    if send_request.id:
        current_message = str(get_request.message)
        current_balance = str(get_request.balance)
        current_interface = str(send_request.event_interface)
        result = {"id": get_request.id, 
                  "interface": current_interface, 
                  "result": current_message,
                  "balance": current_balance
        }
    

        with open('Results.txt', mode = 'a') as f:
            json.dump(result,f)
            f.write('\n')
    else:
        print("Found no feature at %s" % get_request.message)


def Msg_Delivery(stub, request_db):

    global startingport_id
    for request in request_db:
        return request

        

       
    
def run():

    global port_address
# connect to respective ports and send transations   
    for request in request_db:
        print("sending new Transaction request")
        print(request)
        customer_id = request.id
        global startingport_id
        port_id = startingport_id + customer_id
        port_address = str(port_id)
        final_port_address = 'localhost:' + port_address
        
        with grpc.insecure_channel(final_port_address) as channel:
            stub = example_pb2_grpc.TransactionsStub(channel)
            msg_delivery_one(stub, example_pb2.send_request(id=request.id,type=request.type,event_id = request.event_id, 
                        event_interface = request.event_interface, event_money = request.event_money))
            #Msg_Delivery(stub, request_db)
        



    
