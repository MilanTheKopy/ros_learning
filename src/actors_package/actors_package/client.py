import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from interfaces_package.srv import CoolnessTest
import random


class MyClient(Node):

    def __init__(self):
        super().__init__('my_client')

        self.service_client = self.create_client(
            srv_type= CoolnessTest,
            srv_name = 'server',
        )

        self.timer=self.create_timer(
            timer_period_sec=6,
            callback=self.make_service_request
            )

    def make_service_request(self):

        req = CoolnessTest.Request()
        req.name = random.choice(['Milan', 'Terrence', 'Herbert'])
        print(f"We ask for the coolness of: {req.name}")
        future_response = self.service_client.call_async(
            request=req
        )
        future_response.add_done_callback(self.response_callback)
        

    def response_callback(self, future_response):

        response = future_response.result()
        print(f"We got the anwer: {response}")

def main(args=None):
    rclpy.init(args=args)

    my_client = MyClient()

    rclpy.spin(my_client)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    my_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()