from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    window = Node(
        package="turtlesim",
        executable="turtlesim_node"
    )

    turtle_controller = Node(
        package="my_py_pkg",
        executable="turtle_controller",
        parameters=[{"catch_closest":True}]
    )

    turtle_spawner = Node(
        package="my_py_pkg",
        executable="turtle_spawner",
        parameters=[{"spawn_frequency":1.0},{"turtle_name_prefix":"Turtle"}]
    )

    ld.add_action(window)
    ld.add_action(turtle_controller)
    ld.add_action(turtle_spawner)

    return ld