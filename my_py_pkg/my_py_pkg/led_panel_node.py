#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import SetLED
from my_robot_interfaces.msg import LEDStates

class LEDPanelServerNode(Node):

    def __init__(self):
        super().__init__("led_panel")
        self.LED1_ = False
        self.LED2_ = False
        self.LED3_ = False
        self.publisher_ = self.create_publisher(LEDStates,"led_panel_state",10)
        self.timer_ = self.create_timer(2.0,self.publish_led_states)
        self.server_ = self.create_service(SetLED,"set_led",self.callbackSetLED)
        self.get_logger().info("LED panel server has been started.")

    def callbackSetLED(self,request,response):
        self.LED1_ = self.LED1_ ^ request.led1
        self.LED2_ = self.LED2_ ^ request.led2
        self.LED3_ = self.LED3_ ^ request.led3
        response.success = True
        self.get_logger().info("LED states have been changed")
        return response
    
    def publish_led_states(self):
        msg = LEDStates()
        msg.led1 = self.LED1_
        msg.led2 = self.LED2_
        msg.led3 = self.LED3_
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = LEDPanelServerNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()