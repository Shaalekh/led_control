import rclpy
import time
from rclpy.node import Node
from std_srvs.srv import SetBool

class LedControlClass(Node):
    def __init__(self):
        super().__init__('led_control_server')
        self.ledstate=False
        self.clock_state=False
        self.ledsrv=self.create_service(SetBool, 'led_state', self.led_control_callback)
        #tenary operator is used in logging
        self.get_logger().warn("Current Led state: ON" if self.ledstate==True else "Current Led state: OFF")
        
    def led_control_callback(self, request, response):
        requested_state = request.data
        current_state = self.ledstate
        #XOR based problem solving approach
        decision = not requested_state and current_state or requested_state and not current_state
        start_time = time.time()

        #simluate harware delay
        time.sleep(0.9)

        elapsed = time.time() - start_time

        if decision is True:
            if  elapsed < 1.0:
                self.state_trigger()
                response.success = True
                response.message = 'LED turned OFF' if requested_state is False else 'LED turned ON'
            else:
                response.success = False
                response.message = 'Service timed out. Please try again.'
        else:
            response.success = False
            response.message = 'LED is already ON' if requested_state is True else 'LED is already OFF'
            self.get_logger().info(f"Request: {request.data} Response: {response.success}")
        return response
    
    def state_trigger(self):
        self.ledstate = not self.ledstate

    
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