from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    robot_names = ["Giskard","BB8","Daneel","Jander","C3PO"]

    for i in range(5):
        news_node = Node(
            package="my_py_pkg",
            executable="robot_news_station",
            name="robot_news_station_"+str.lower(robot_names[i]),
            parameters=[{"robot_name":robot_names[i]}]
        )
        ld.add_action(news_node)

    smartphone_node = Node(
        package="my_py_pkg",
        executable="smartphone",
        name="smartphone",
    )

    ld.add_action(smartphone_node)

    return ld