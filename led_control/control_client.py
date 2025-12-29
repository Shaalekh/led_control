import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool
from std_srvs.srv import Trigger

class ControlClientClass(Node):
    def __init__(self):
        super().__init__('control_client')
        self.create_client(SetBool, 'led_control_server')

        