import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool
from std_srvs.srv import Trigger

class ControlClientClass(Node):
    def __init__(self):
        super().__init__('control_client')
        self.get_logger().debug("Client Node is Initiated")
        self.led_cli = self.create_client(SetBool, 'led_control')
        self.pwr_cli = self.create_client(Trigger, 'power_check')
        self.sft_cli = self.create_client(Trigger, 'safety_check')
        #wait_for_service to be active
        while not self.led_cli.wait_for_service(1):
            self.get_logger().info('led_control service not available, waiting...')
            
    def send_request(self):
        request=SetBool.Request()
        request.data=True
        return self.led_cli.call_async(request)
    
    def _request_pwr_check(self):
        while not self.led_cli.wait_for_service(1.0):
            self.get_logger().info('power_check service is not available, waiting...')
        request=Trigger.Request()
        future = self.pwr_cli.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        response=future.result()
        return response.success, response.message
    
    def _request_sft_check(self):
        while not self.sft_cli.wait_for_service(1.0):
            self.get_logger().info('safety_check service is not available, waiting...')
        request=Trigger.Request()
        future = self.sft_cli.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        response=future.result()
        return response.success, response.message
    
def main():
    rclpy.init()
    node=ControlClientClass()
    try:
        power_response = node._request_pwr_check()
        safety_response = node._request_sft_check()
        if safety_response[0] and power_response[0]:
            future=node.send_request()
            rclpy.spin_until_future_complete(node, future)
            response=future.result()
            node.get_logger().info(f'{response.success} {response.message}')
        else:
            node.get_logger().info(f'[{safety_response[1]} | {power_response[1]}]')
    except Exception as e:
        node.get_logger().error(e)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()