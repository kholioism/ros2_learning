#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from my_robot_interfaces.msg import Turtle,TurtleArray
from my_robot_interfaces.srv import CatchTurtle
import math
from functools import partial

class TurtleControllerNode(Node):

    def __init__(self):
        super().__init__("turtle_controller")
        self.target = None
        self.pose = None
        self.declare_parameter("catch_closest",True)
        self.catch_closest = self.get_parameter("catch_closest").value
        self.publisher_ = self.create_publisher(Twist,"turtle1/cmd_vel",10)
        self.timer_ = self.create_timer(0.01,self.publishTwist)
        self.pose_subscription_ = self.create_subscription(Pose,"turtle1/pose",self.callbackPose,10)
        self.turtle_subscriber_ = self.create_subscription(
            TurtleArray,"alive_turtles",self.callbackAlive,10)


    def publishTwist(self):
        if self.pose == None or self.target == None:
            return
        dist_x = self.target.x - self.pose.x
        dist_y = self.target.y - self.pose.y
        distance = math.sqrt(dist_x**2+dist_y**2)
        goal_theta = math.atan2(dist_y,dist_x)
        diff_theta = goal_theta - self.pose.theta
        if diff_theta>math.pi:
            diff_theta-=2*math.pi
        elif diff_theta<-math.pi:
            diff_theta+=2*math.pi

        msg = Twist()

        if distance>0.5:
            msg.linear.x = 2*distance
            msg.angular.z = 6*diff_theta
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.callCatchTurtleServer(self.target.name)
            self.target = None

        self.publisher_.publish(msg)

    def callbackPose(self,msg):
        self.pose = msg

    def callbackAlive(self,msg):
        if self.pose == None:
            return
        if len(msg.turtles)>0:
            if not self.catch_closest:
                self.target = msg.turtles[0]
            else:
                closest_turtle = None
                closest_distance = None
                for turtle in msg.turtles:
                    dist_x = turtle.x - self.pose.x
                    dist_y = turtle.y - self.pose.y
                    distance = math.sqrt(dist_x**2+dist_y**2)
                    if closest_turtle == None or distance<closest_distance:
                        closest_turtle = turtle
                        closest_distance = distance
                self.target = closest_turtle


    def callCatchTurtleServer(self,turtle_name):
        client = self.create_client(CatchTurtle,"catch_turtle")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Wait for catch...")

        request = CatchTurtle.Request()
        request.name = turtle_name

        future = client.call_async(request)
        future.add_done_callback(partial(self.callbackCatchTurtle,turtle_name=turtle_name))

    def callbackCatchTurtle(self,future,turtle_name):
        try:
            response = future.result()
            if response.success:
                self.get_logger().info(turtle_name+" has been caught.")
            else:
                self.get_logger().error(turtle_name+" hasn't been caught.")
        except Exception as e:
            self.get_logger().error("Service call failed %r"%(e,))

def main(args=None):
    rclpy.init(args=args)
    node = TurtleControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()