from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
import os
from ament_index_python.packages import get_package_share_path
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    
    rviz = os.path.join(get_package_share_path('my_robot_description'),'rviz','urdf_config.rviz')
    
    urdf = os.path.join(get_package_share_path('my_robot_description'),'urdf','my_robot.urdf.xacro')

    yaml = os.path.join(get_package_share_path('my_robot_bringup'),'config','my_robot.yaml')

    robot_description = ParameterValue(Command(['xacro ', urdf]),value_type=str)

    ros_gz_sim_pkg_path = get_package_share_directory('ros_gz_sim')


    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{'robot_description':robot_description}]
    )

    gazebo = Node(

    )

    start_gazebo_ros_bridge_cmd = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={yaml}',
        ],
        output='screen',
    )

    start_gazebo_ros_image_bridge_cmd = Node(
        package='ros_gz_image',
        executable='image_bridge',
        arguments=['/camera/image_raw'],
        output='screen',
    )

    gz_sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([ros_gz_sim_pkg_path, 'launch', 'gz_sim.launch.py'])
        ),
        launch_arguments={
            'gz_args': 'empty.sdf -r'
        }.items()
    )
    
    create_node = Node(
        package='ros_gz_sim',
        executable='create',
        name='create',
        arguments=['-topic', 'robot_description'],
        output='screen'
    )

    rviz2 = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', rviz]
    )

    return LaunchDescription(
        [robot_state_publisher,
        rviz2,
        start_gazebo_ros_image_bridge_cmd,
        gz_sim_launch,
        create_node,
        start_gazebo_ros_bridge_cmd]
    )