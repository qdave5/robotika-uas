# ref: https://gist.github.com/leander-dsouza/c691dcdcee33864f5209437a56cf059f

# instalasi py_trees_ros: https://github.com/splintered-reality/py_trees_ros?tab=readme-ov-file
# $ sudo 

#! /usr/bin/env python3
"""
Teleoperation using arrow keys for ROS2
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import keyboard

KEY_BIND = {
    'UP': ['a', 'up'],
    'DOWN': ['s','down'],
    'RIGHT': ['d', 'right'],
    'LEFT': ['a','left'],
}


class Keyboard(Node):
    """
    Class to teleoperate the robot
    """
    def __init__(self):
        super().__init__('keyboard')

        self.update_rate = 50
        self.time_period = 1./self.update_rate

        self.max_linear_velocity = 1.5
        self.max_angular_velocity = 2.5
        self.obj = Twist()

        # Publishers
        self.pub = self.create_publisher(Twist, "/cmd_vel", \
            qos_profile_unlatched())

        # Timers
        self.timer = self.create_timer(self.time_period, self.keyboard_update)

    def forward(self):
        """
        Move Forward
        """
        print('forward')
        self.obj.linear.x = float(self.max_linear_velocity)
        self.obj.angular.z = 0.0
        self.pub.publish(self.obj)

    def backward(self):
        """
        Move Backward
        """
        print('backward')
        self.obj.linear.x = float(-self.max_linear_velocity/2)
        self.obj.angular.z = 0.0
        self.pub.publish(self.obj)

    def left(self):
        """
        Move Left
        """
        print('left')
        self.obj.linear.x = 0.0
        self.obj.angular.z = float(self.max_angular_velocity)
        self.pub.publish(self.obj)

    def right(self):
        """
        Move Right
        """
        print('right')
        self.obj.linear.x = 0.0
        self.obj.angular.z = float(-self.max_angular_velocity)
        self.pub.publish(self.obj)

    def brutestop(self):
        """
        Stop the robot
        """
        self.obj = Twist()
        self.pub.publish(self.obj)

    def key_press(self, key):
        """
        Listen for key press
        """
        if key.name == KEY_BIND['UP'][0] or key.name == KEY_BIND['UP'][1]:
            self.forward()
        elif key.name == KEY_BIND['DOWN'][0] or key.name == KEY_BIND['DOWN'][1]:
            self.backward()
        elif key.name == KEY_BIND['RIGHT'][0] or key.name == KEY_BIND['RIGHT'][1]:
            self.right()
        elif key.name == KEY_BIND['LEFT'][0] or key.name == KEY_BIND['LEFT'][1]:
            self.left()

        # if key == Key.up:
        #     self.forward()
        # elif key == Key.down:
        #     self.backward()
        # elif key == Key.right:
        #     self.right()
        # elif key == Key.left:
        #     self.left()
        # return False

    def key_release(self, key):
        """
        Listen for key release
        """
        self.brutestop()
        return False

    def keyboard_update(self):
        """
        Keyboard Listener for a press and release
        """
        print('keyboard')

        keyboard.on_press(key_press)

        # with keyboard.Listener(on_press=self.key_press) \
        #     as listener_for_key_press:
        #     listener_for_key_press.join()

        # with keyboard.Listener(on_release=self.key_release) \
        #     as listener_for_key_release:
        #     listener_for_key_release.join()

def main(args=None):
    """
    Main Function
    """
    rclpy.init(args=args)

    keyboard = Keyboard()
    rclpy.spin(keyboard)

    keyboard.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()