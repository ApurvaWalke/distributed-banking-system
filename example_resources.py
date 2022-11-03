
import json

import example_pb2


def read_example_database():
    """Reads the  database and returns the request list
  """
    request_list = []
    with open("example_db.json") as example_db_file:
        for item in json.load(example_db_file):
          if item["type"] == "customer":
            event_list = item["events"]
            for i in range (0,len(event_list)):
              event_id = event_list[i]["id"]
              event_interface = event_list[i]["interface"]
              event_money = event_list[i]["money"]
              request = example_pb2.send_request(id=item["id"],type=item["type"],event_id = event_id, 
                        event_interface = event_interface, event_money = event_money) 
              #print("line 27 in example_resources.py")
              request_list.append(request)
            #print(request)
    return request_list
    
