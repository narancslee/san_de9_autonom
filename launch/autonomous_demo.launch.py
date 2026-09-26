"""Launch the autonomous robot demonstration."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """Create the launch description."""
    return LaunchDescription([
        Node(
            package='san_de9_autonom',
            executable='robot_simulator',
            output='screen',
        ),
        Node(
            package='san_de9_autonom',
            executable='waypoint_controller',
            output='screen',
            parameters=[
                {'goal_x': 5.0},
            ],
        ),
    ])
