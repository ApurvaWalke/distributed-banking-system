# Project Summary

The goal is to develop a distributed banking system that allows multiple customers to withdraw or deposit money from the multiple branches in the bank. Each branch is on different server. Some of the key assumptions are:
1. One customer to communicate with only a specific branch that has the same unique ID as itself
2. Although each customer independently updates a specific replica, the replicas stored in each branch need to reflect all the updates made by the customer.
3. No concurrent updates on the same resources (money) in the bank
4. No customer accesses multiple branches



## To run the project: 

1. main.py is the main python file to start with
2. example_db.json has the input
3. example.proto has the protocol buffer definitons
4. All branches start with the inital balance of 400 dollars
5. On running the main.py file it will call all the files to sequentially open tthe server ports, get the clients connected with the server and handle all the ttransactions
6. Results.txt file is written at the end with the summary and status for all the transactions.



