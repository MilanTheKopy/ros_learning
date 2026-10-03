import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from ros_gz_bridge.actions import RosGzBridge


def generate_launch_description():

    # -------------------------
    # Paths
    # -------------------------

    simulation_pkg = get_package_share_directory('simulation_package')
    ros_gz_sim_pkg = get_package_share_directory('ros_gz_sim')

    world_path = os.path.join(
        simulation_pkg,
        'worlds',
        'segway_world.sdf'
    )

    models_path = os.path.join(
        simulation_pkg,
        'models'
    )

    gz_launch_path = os.path.join(
        ros_gz_sim_pkg,
        'launch',
        'gz_sim.launch.py'
    )

    # -------------------------
    # Gazebo
    # -------------------------
    gazebo_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=models_path
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_launch_path),
        launch_arguments={
            'gz_args': f'-r {world_path}'
        }.items()
    )

    # -------------------------
    # Gazebo <-> ROS bridge
    # -------------------------
    """
    bridge_config = os.path.join(
            get_package_share_directory('sensor_tutorial'),
            'config',
            'bridge_config.yaml'
        ) 
    bridge = RosGzBridge(
        bridge_name='ros_gz_bridge',
        config_file=bridge_config,
    )
    
    # -------------------------
    # Your ROS Python nodes
    # -------------------------

    controller_node = Node(
        package='sensor_tutorial',
        namespace='sensor_tutorial',
        executable='controller',
        name='controller',
        output='screen'
    )
    """
    return LaunchDescription([
        gazebo_resource_path,
        gazebo,
        #bridge,
        #controller_node,
        
    ])