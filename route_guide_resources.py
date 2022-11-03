
import json

import example_pb2


def read_route_guide_database():
    """Reads the route guide database.
  Returns:
    The full contents of the route guide database as a sequence of
      route_guide_pb2.Features.
  """
    feature_list = []
    with open("example_db.json") as example_db_file:
        for item in json.load(example_db_file):
            feature = example_pb2.Feature(
                name=item["name"],
                message=example_pb2.Point(
                    id=item["location"]["latitude"],
                    message=item["location"]["longitude"]))
            feature_list.append(feature)
    return feature_list
