import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool
from std_srvs.srv import Trigger

class ControlClientClass(Node):
    def __init__(self):
        super().__init__('control_client')
        self.con_cli = self.create_client(SetBool, 'led_control')

    def wait_for_service(self):
        while not self.con_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
            
    def send_request(self):
        self.request=SetBool.Request()
        self.request.data=True
        return self.con_cli.call_async(self.request)
    
def main():
    rclpy.init()
    node=ControlClientClass()
    node.wait_for_service()
    try:
        future=node.send_request()
        rclpy.spin_until_future_complete(node, future)
        response=future.result()
        node.get_logger().info(f'{response.success} {response.message}')
    except Exception as e:
        node.get_logger().error(e)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()