#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import SetBool
from functools import partial

class BooleanClientNode(Node):

    def __init__(self):
        super().__init__("add_two_ints_client")
        self.callBooleanServer(True)

    def callBooleanServer(self,data):
        client = self.create_client(SetBool,"reset_counter")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Wait for server Set Bool...")

        request = SetBool.Request()
        request.data = data

        future = client.call_async(request)
        future.add_done_callback(partial(self.callbackSetBool,data=data))

    def callbackSetBool(self,future,data):
        try:
            response = future.result
            self.get_logger().info(str(data)+" sent.")
        except Exception as e:
            self.get_logger().error("Service call failed %r"%(e,))


def main(args=None):
    rclpy.init(args=args)
    node = BooleanClientNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()