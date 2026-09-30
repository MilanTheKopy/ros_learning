import os

from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node


def generate_launch_description():
    config = os.path.join(
        get_package_share_directory('actors_package'),
        'config',
        'params.yaml'
    ) #laedt die parameter


    return LaunchDescription([

        Node(
            package='actors_package',
            namespace='server_client',
            executable='client',
            name='client'
        ),
        Node(
            package='actors_package',
            namespace='server_client',
            executable='server',
            name='server',
            parameters=[config],
        ),

    ])