#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import SetLED
from functools import partial

class BatteryClientNode(Node):

    def __init__(self):
        super().__init__("battery_client")
        self.callSetLEDServer(False,False,True)

    def callSetLEDServer(self,LED1,LED2,LED3):
        client = self.create_client(SetLED,"set_led")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Wait for server SetLED...")

        request = SetLED.Request()
        request.led1 = LED1
        request.led2 = LED2
        request.led3 = LED3

        future = client.call_async(request)
        future.add_done_callback(partial(self.callbackSetLED))

    def callbackSetLED(self,future):
        try:
            response = future.result()
            self.get_logger().info("LED states changed")
        except Exception as e:
            self.get_logger().error("Service call failed %r"%(e,))


def main(args=None):
    rclpy.init(args=args)
    node = BatteryClientNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()