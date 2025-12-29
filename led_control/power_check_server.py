import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

''' Here, you can import SetBool type but make sure that
    you don't read request.data inside callback function.
    Directly set response.success based on power status.
'''
class PowerCheckServerClass(Node):
    def __init__(self):
        super().__init__('power_check')
        # power_status True indicates power is sufficient if False means low power
        # Set it based on your requirement or create a function that directly reads power status from hardware

        self.power_status=True
        self.create_service(Trigger, 'power_check', self.power_check_callback)
        self.get_logger().info("Power Check Service is active and running.")

    def power_check_callback(self, request, response):
        response.success = True if self.power_status else False
        response.message = "Power Check OK" if self.power_status else "Low Power Detected"

        self.get_logger().info(f'CheckUp requested, Response: {response.message}')
        return response
    


def main():
    try:
        rclpy.init()
        node=PowerCheckServerClass()
        rclpy.spin(node)
        node.destroy_node()
        rclpy.shutdown()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        node.get_logger().error(e)

if __name__=='__main__':
    main()
        