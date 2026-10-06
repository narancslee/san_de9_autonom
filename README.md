# san_de9_autonom

ROS 2 Python project demonstrating a simple autonomous waypoint controller.

The project contains two nodes:

- `robot_simulator` simulates a robot moving on the x axis.
- `waypoint_controller` uses odometry feedback to drive the robot toward a target position.

## ROS topics

`robot_simulator` subscribes to:

- `/cmd_vel` (`geometry_msgs/Twist`)

and publishes:

- `/odom` (`nav_msgs/Odometry`)

`waypoint_controller` subscribes to:

- `/odom` (`nav_msgs/Odometry`)

and publishes:

- `/cmd_vel` (`geometry_msgs/Twist`)

The two nodes form a simple closed feedback loop.

## Controller

The default target is:

    goal_x = 5.0 m

The controller uses proportional control and limits the commanded velocity to 1.0 m/s.

The robot stops when it is within 0.05 m of the target.

## Build

From a ROS 2 workspace:

    colcon build --packages-select san_de9_autonom --symlink-install
    source install/setup.bash

## Run

    ros2 launch san_de9_autonom autonomous_demo.launch.py

A different target can later be configured through the `goal_x` ROS parameter.
