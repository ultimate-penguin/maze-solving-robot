import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'maze_bot'
    pkg_share = get_package_share_directory(pkg_name)
    
    world_path = os.path.join(pkg_share, 'worlds', 'maze_generated.sdf')
    urdf_path = os.path.join(pkg_share, 'urdf', 'robot.urdf')

    return LaunchDescription([
        # 1. Start Gazebo Harmonic with the maze world
        ExecuteProcess(
            cmd=['gz', 'sim', world_path],
            output='screen'
        ),

        # 2. Spawn the robot into Gazebo
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-file', urdf_path, '-x', '-2', '-y', '-2.4', '-z', '0.2'],
            output='screen'
        ),
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=['/lidar@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan'],
            remappings=[('/lidar', '/scan')],
            output='screen'
        ),
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=['/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist'],
            output='screen'
        )
    ])