import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool

class LedControlClass(Node):
    def __init__(self):
        super().__init__('led_control_server')
        self.ledstate=False
        self.ledsrv=self.create_service(SetBool, 'led_state', self.xor_callback)
        #tenary operator is used in logging
        self.get_logger().warn("Current Led state: ON" if self.ledstate==True else "Current Led state: OFF")
        
    def xor_callback(self, request, response):
        a = request.data
        b = self.ledstate
        c = not a and b or a and not b
        if c is True:
            self.state_trigger()
            response.success = True
            response.message = 'LED turned OFF' if a is False else 'LED turned ON'
        else:
            response.success = False
            response.message = 'LED is already ON' if a is True else 'LED is already OFF'
        print("Response:", response.success, type(response.success))
        
        return response
    
    def state_trigger(self):
        self.ledstate = not self.ledstate
        print(self.ledstate)

    
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