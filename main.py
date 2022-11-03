from __future__ import print_function
import random
from concurrent import futures
import time
import math
import logging
import os
import grpc
import multiprocessing
import example_pb2
import example_pb2_grpc
import example_resources
import Branch
import Customer


request_db = example_resources.read_example_database()


def get_unique_branch_ids(): #get unique ids from the input json file to open server ports
    request_id = []
    for request in request_db:
        request_id.append(request.id)
    #global unique_id
    unique_branch_id = set(request_id)
    return unique_branch_id


unique_id = []
if __name__ == "__main__":

    unique_id = get_unique_branch_ids()

    pid = []
    
    #Opening server ports for connection using multiprocessing
    for i in unique_id:
        process = multiprocessing.Process(target=Branch.serve, args=(i, ))  
        pid.append(process)
        # starting process 1
        process.start()
        time.sleep(5)

    time.sleep(5)
    
    #Calling customer.py file to run all the transaction

    Customer.run()

    print("Executed all the transactions. Output present in Results.txt file. Please exit the code")

    for id in pid:
        id.join()

  
    # both processes finished
    
