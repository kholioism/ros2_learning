#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import TurtleArray, Turtle
from my_robot_interfaces.srv import CatchTurtle
from turtlesim.srv import Spawn, Kill
from random import uniform
from functools import partial
from math import pi

class TurtleSpawnerNode(Node):

    def __init__(self):
        super().__init__("turtle_spawner")
        self.declare_parameter("spawn_frequency",1.0)
        self.declare_parameter("turtle_name_prefix","turtle")
        self.frequency_ = self.get_parameter("spawn_frequency").value
        self.turtle_number = 1
        self.turtles = []
        self.prefix_ = self.get_parameter("turtle_name_prefix").value
        self.publisher_ = self.create_publisher(TurtleArray, "alive_turtles", 10)
        self.spawn_timer_ = self.create_timer(1.0/self.frequency_, self.spawnNew)
        self.catch_turtle_ = self.create_service(CatchTurtle, "catch_turtle", self.callbackCatchTurtle)

    def spawnNew(self):
        self.turtle_number += 1
        self.callSpawnServer(uniform(0.0, 11.0), uniform(0.0, 11.0), uniform(0.0, 2 * pi),
                             self.prefix_ + str(self.turtle_number))

    def callSpawnServer(self, x, y, theta, turtle_name):
        client = self.create_client(Spawn, "spawn")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for spawn service...")

        request = Spawn.Request()
        request.x = x
        request.y = y
        request.theta = theta
        request.name = turtle_name

        future = client.call_async(request)
        future.add_done_callback(partial(self.callbackSpawn, x=x, y=y, theta=theta, turtle_name=turtle_name))

    def callbackSpawn(self, future, x, y, theta, turtle_name):
        try:
            response = future.result()
            self.callbackPublishTurtles()
            if response.name != "":
                self.get_logger().info("Turtle " + response.name + " is now alive.")
                self.turtles.append(Turtle(name=turtle_name, x=x, y=y, theta=theta))  # Correct Turtle msg usage
        except Exception as e:
            self.get_logger().error(f"Spawn service call failed: {e}")

    def callKillServer(self, turtle_name):
        client = self.create_client(Kill, "kill")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for kill service...")

        request = Kill.Request()
        request.name = turtle_name

        future = client.call_async(request)
        future.add_done_callback(partial(self.callbackKill, turtle_name=turtle_name))

    def callbackKill(self, future, turtle_name):
        try:
            future.result()
            self.turtles = [turtle for turtle in self.turtles if turtle.name != turtle_name]
            self.callbackPublishTurtles()
            self.get_logger().info(f"Turtle {turtle_name} has been caught.")
        except Exception as e:
            self.get_logger().error(f"Kill service call failed: {e}")

    def callbackCatchTurtle(self, request, response):
        self.callKillServer(request.name)
        response.success = True
        return response

    def callbackPublishTurtles(self):
        msg = TurtleArray()
        msg.turtles = self.turtles
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawnerNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
