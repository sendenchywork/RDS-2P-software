"""Forward ROS motor commands to the browser diagnostic subscriber."""
import argparse
import json

import rclpy
import zenoh
from ftservo_ros.msg import MotorCommands
from rclpy.node import Node
from rosidl_runtime_py.convert import message_to_ordereddict

KEY = "rds2p/sim/motors/commands"

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--endpoint", default="tcp/127.0.0.1:7447")
    args = parser.parse_args()
    config = zenoh.Config()
    config.insert_json5("mode", '"client"')
    config.insert_json5("connect/endpoints", json.dumps([args.endpoint]))
    with zenoh.open(config) as session, rclpy.init():
        node = Node("rds2p_web_bridge")
        def forward(message):
            try:
                payload = json.dumps(message_to_ordereddict(message), allow_nan=False)
            except ValueError as error:
                node.get_logger().warning(f"Invalid motor command: {error}")
                return
            session.put(KEY, payload, encoding=zenoh.Encoding.APPLICATION_JSON)

        node.create_subscription(MotorCommands, "/motors/commands", forward, 10)
        try:
            rclpy.spin(node)
        finally:
            node.destroy_node()


if __name__ == "__main__":
    main()
