from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
import os
from ament_index_python.packages import get_package_share_path

def generate_launch_description():
    
    rviz = os.path.join(get_package_share_path('my_robot_description'),'rviz','urdf_config.rviz')
    
    urdf = os.path.join(get_package_share_path('my_robot_description'),'urdf','my_robot.urdf.xacro')

    robot_description = ParameterValue(Command(['xacro ', urdf]),value_type=str)

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{'robot_description':robot_description}]
    )

    joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui"
    )

    rviz2 = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', rviz]
    )

    return LaunchDescription(
        [robot_state_publisher,
        joint_state_publisher_gui,
        rviz2]
    )