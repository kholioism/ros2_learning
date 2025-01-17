#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from example_interfaces.msg import String
from example_interfaces.srv import SetBool

class NumberCounter(Node):

    def __init__(self):
        super().__init__("number_counter")
        self.count_ = 0
        self.publisher_ = self.create_publisher(String,"number_count", 10)        
        self.subscriber_ = self.create_subscription(String,"number",self.callback_robot_news,10)
        self.server_ = self.create_service(SetBool,"reset_counter",self.callback_reset_counter)
        self.get_logger().info("Number counter has started.")

    def publish_number(self):
        msg = String()
        self.count_ += 1
        msg.data = str(self.count_)
        self.publisher_.publish(msg)

    def callback_robot_news(self,msg):
        self.get_logger().info(msg.data)
        self.publish_number()
    
    def callback_reset_counter(self,request,response):
        if request.data:
            self.count_ = 0
            response.success = True
            response.message = "Counter has been reset."
        else:
            response.success = False
            response.message = "Counter reset request denied."
        return response

def main(args=None):
    rclpy.init(args=args)
    node = NumberCounter()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()