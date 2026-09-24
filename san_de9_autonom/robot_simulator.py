"""Simple 1D robot simulator for ROS 2."""

import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node


class RobotSimulator(Node):
    """Simulate a robot moving along the x axis."""

    UPDATE_PERIOD = 0.1
    COMMAND_TIMEOUT = 1.0

    def __init__(self):
        super().__init__('robot_simulator')

        self.position = 0.0
        self.velocity = 0.0
        self.last_command_time = self.get_clock().now()

        self.odom_publisher = self.create_publisher(
            Odometry,
            'odom',
            10,
        )

        self.cmd_subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            10,
        )

        self.timer = self.create_timer(
            self.UPDATE_PERIOD,
            self.update_robot,
        )

    def cmd_vel_callback(self, msg):
        """Store the latest commanded velocity."""
        self.velocity = msg.linear.x
        self.last_command_time = self.get_clock().now()

    def update_robot(self):
        """Update robot position and publish odometry."""
        now = self.get_clock().now()

        command_age = (
            now - self.last_command_time
        ).nanoseconds / 1e9

        if command_age > self.COMMAND_TIMEOUT:
            self.velocity = 0.0

        self.position += self.velocity * self.UPDATE_PERIOD

        odom = Odometry()
        odom.header.stamp = now.to_msg()
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'

        odom.pose.pose.position.x = self.position
        odom.pose.pose.orientation.w = 1.0

        odom.twist.twist.linear.x = self.velocity

        self.odom_publisher.publish(odom)


def main(args=None):
    """Run the robot simulator node."""
    rclpy.init(args=args)
    node = RobotSimulator()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
