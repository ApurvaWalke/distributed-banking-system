
from __future__ import print_function
import random
from concurrent import futures
import time
import math
import logging
import grpc
import example_pb2
import example_pb2_grpc
import example_resources
import argparse
import sys
import main



branch_balance = 400
branch_id = id
startingport_id = 50050 
branch_ids = main.get_unique_branch_ids()
branch_ids_str = []
for ids in branch_ids:
    branch_ids_str.append(str(ids))
branch_ledger_dic = {branch_ids_str[i]: 400 for i in range(len(branch_ids_str))}


# Propogate current branch balance to all the branches
def branch_propogate_balance(stub, send_request):
    get_request = stub.MsgDelivery(send_request)
    return "Process complete??"

# Most important method. Gets the request from customer.py and according to request type will execute the transaction and return the response
def Msg_Delivery(self, send_request):
    """Returns Feature at given location or None."""
    #print(send_request.event_interface)
    global branch_balance
    if send_request.event_interface: 
        if send_request.event_interface == "withdraw":
            branch_balance = branch_balance - send_request.event_money
            #propogate balance to all the brances
            for i in branch_ids:
                if send_request.id == branch_id: 
                    branch_balance_ledger(i, branch_balance)
                else:
                    startingport_id = 50050 
                    port_id = startingport_id + i
                    port_address = str(port_id)
                    final_port_address = 'localhost:' + port_address
                    with grpc.insecure_channel(final_port_address) as channel:
                        stub = example_pb2_grpc.TransactionsStub(channel)
                        branch_propogate_balance(stub, example_pb2.send_request(id=send_request.id,balance = 				 branch_balance))
            response = example_pb2.get_response(id = send_request.id, balance = branch_balance, message = "Withdraw 	     Transaction successfull" )
            return response
            
        # No propogation method called for query request
        elif send_request.event_interface == "query":
            branch_balance = branch_balance
            response = example_pb2.get_response(id = send_request.id, balance = branch_balance, message = "Withdraw Transaction successfull" )
            print ("No propogation request for query transaction")
            return response

        elif send_request.event_interface == "deposit":
            branch_balance = branch_balance + send_request.event_money
            #propogate balance to all the brances
            for i in branch_ids:
                if i == branch_id: 
                    branch_balance_ledger(i, branch_balance)
                else:
                    startingport_id = 50050 
                    port_id = startingport_id + i
                    port_address = str(port_id)
                    final_port_address = 'localhost:' + port_address
                    with grpc.insecure_channel(final_port_address) as channel:
                        stub = example_pb2_grpc.TransactionsStub(channel)
                        branch_propogate_balance(stub, example_pb2.send_request(id=send_request.id,balance = branch_balance))
                        response = example_pb2.get_response(id = send_request.id, balance = branch_balance, message = "Deposit Transaction successfull" )
                        return response 
        #propogate balance to all the brances
        for i in branch_ids:
            if i == branch_id: 
                test =  branch_balance_ledger(send_request.id, send_request.balance)
                print("update current branch id ledger")
            else:
                startingport_id = 50050 
                port_id = startingport_id + i
                port_address = str(port_id)
                final_port_address = 'localhost:' + port_address
                with grpc.insecure_channel(final_port_address) as channel:
                    stub = example_pb2_grpc.TransactionsStub(channel)
                    branch_propogate_balance(stub, example_pb2.send_request(id=request.id,balance = branch_balance))

        response = example_pb2.get_response(id = send_request.id, balance = branch_balance, message = "Query Transaction successfull" )
    elif send_request.balance:
        test =  branch_balance_ledger(send_request.id, send_request.balance)
        response = example_pb2.get_response(id= send_request.id, balance  = send_request.balance, message = "Propageted balance")
    else:
        response = example_pb2.get_response(id = 1, balance = branch_balance, message = "Unknown Interface" )

    return response

# a dictionary to keep tab of the current balance status for all the branches
def branch_balance_ledger(b_id, balance):
    # update dictionary for particular ID
    global branch_ledger_dic
    branch_ledger_dic[(str(b_id))] = balance
    print ("waiting 3 seconds to update all branches")
    time.sleep(3)
    print ("Printing current balance for all branches")
    for i in branch_ledger_dic:
        print (i, branch_ledger_dic[i])
    return balance




class ExampleServicer(example_pb2_grpc.TransactionsServicer):
    """Provides methods that implement functionality of route guide server."""

    
    def __init__(self, id =1):

        self.id = id
        branch_id = id

    def MsgDelivery(self, request, context):

        if request.id == self.id:
            get_response = Msg_Delivery(self,request)
        elif request.balance:
            get_response = Msg_Delivery(self,request)
        else:
            return example_pb2.get_response(message="Connecting to wrong server", id =request)
        if get_response is None:
            return example_pb2.get_response(message="Something went wrong here", id =request)

        else:
            return get_response


# Creating server connections 
def serve(id = 1):

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_TransactionsServicer_to_server(ExampleServicer(id), server)
    global startingport_id
    port_id = startingport_id + id
    port_address = str(port_id)
    print("Printing port address")
    print('[::]:' + port_address)
    server.add_insecure_port('[::]:' + port_address )
    server.start()
    print ("server is listing ...")
    server.wait_for_termination()
    


    
