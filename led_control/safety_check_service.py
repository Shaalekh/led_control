import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

class SafetyCheckServerClass(Node):
    def __init__(self):
        super().__init__('safety_check_server')
        self.emergency_stop_status=False
        self.create_service(Trigger, 'safety_check', self.safety_check_callback)
        self.get_logger().info("Safety Check Server is active and running")

    def safety_check_callback(self, request , response):
        response.success = False if self.emergency_stop_status else True
        response.message = "Emergency Stop Activated" if self.emergency_stop_status else "Safety Check OK"

        self.get_logger().info(f"Safety Check Response: {response.message}")

        return response

def main() -> None:
    try:
        rclpy.init()
        node=SafetyCheckServerClass()
        rclpy.spin(node)
        node.destroy_node()
        rclpy.shutdown()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        node.get_logger().error(e)

if __name__=='__main__':
    main()