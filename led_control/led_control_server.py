import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool

class LedControlClass(Node):
    def __init__(self):
        super().__init__('led_control_server')
        self.ledstate=False
        self.ledsrv=self.create_service(SetBool, 'led_control', self.led_control_callback)
        #tenary operator is used in logging
        self.get_logger().info("Led Control Server is active and Running.")
        self.get_logger().warn("Current Led state: ON" if self.ledstate==True else "Current Led state: OFF")
        
    def led_control_callback(self, request, response):
        a = request.data
        b = self.ledstate
        c = not a and b or a and not b
        if c is True:
            self.ledstate = not self.ledstate
            response.success = True
            response.message = 'LED turned OFF' if a is False else 'LED turned ON'
        else:
            response.success = False
            response.message = 'LED is already ON' if a is True else 'LED is already OFF'
        self.get_logger().info(f'Request: {"Turn ON" if request.data else "Turn OFF"}  Response: {response.message}')
        
        return response
    

    
def main() -> None:
    try:
        rclpy.init()
        server=LedControlClass()
        rclpy.spin(server)
        server.destroy_node()
        rclpy.shutdown()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)

if __name__=='__main__':
    main()