"""Waypoint controller for a simulated 1D robot."""

import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node


class WaypointController(Node):
    """Drive the robot toward a target x position."""

    KP = 0.8
    MAX_SPEED = 1.0
    GOAL_TOLERANCE = 0.05

    def __init__(self):
        super().__init__('waypoint_controller')

        self.declare_parameter('goal_x', 5.0)
        self.goal_x = self.get_parameter('goal_x').value

        self.cmd_publisher = self.create_publisher(
            Twist,
            'cmd_vel',
            10,
        )

        self.odom_subscription = self.create_subscription(
            Odometry,
            'odom',
            self.odom_callback,
            10,
        )

        self.goal_reached = False

        self.get_logger().info(
            f'Target position: x = {self.goal_x:.2f} m'
        )

    def odom_callback(self, msg):
        """Calculate and publish a velocity command."""
        position = msg.pose.pose.position.x
        error = self.goal_x - position

        command = Twist()

        if abs(error) <= self.GOAL_TOLERANCE:
            command.linear.x = 0.0

            if not self.goal_reached:
                self.get_logger().info(
                    f'Goal reached at x = {position:.2f} m'
                )
                self.goal_reached = True
        else:
            self.goal_reached = False

            velocity = self.KP * error
            velocity = max(
                -self.MAX_SPEED,
                min(self.MAX_SPEED, velocity),
            )

            command.linear.x = velocity

        self.cmd_publisher.publish(command)


def main(args=None):
    """Run the waypoint controller node."""
    rclpy.init(args=args)
    node = WaypointController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
