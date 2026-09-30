import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
from std_msgs.msg import String
from interfaces_package.srv import CoolnessTest


class MyService(Node):

    def __init__(self):
        super().__init__('my_service')

        self.declare_parameter('coolness_bonus', 0)
        self.add_on_set_parameters_callback(self.parameter_callback)
        self.service = self.create_service(
            srv_type=CoolnessTest,
            srv_name='server',
            callback=self.service_callback
        )


    def parameter_callback(self, params):
        result = SetParametersResult(successful=True)
        result.reason = 'Fine'

        for param in params:
            if param.name ==  'coolness_bonus' and param.value < 0:
                result.successful = False #somit wird die aenderung auch nicht ausgefuehrt
                result.reason = 'coolness_bonus has to be > 0'

            else:            
                self.get_logger().info(f"{param.name} was set to {param.value}")
        return result

    
    def service_callback(self, request, response):

        if request.name == 'Milan':
            response.level = 10 + int(self.get_parameter('coolness_bonus').value)
        else:
            response.level = 0 + int(self.get_parameter('coolness_bonus').value)

        self.get_logger().info(f'Coolness Level for {request.name}: {response.level}')

        return response
        


def main(args=None):
    rclpy.init(args=args)

    minimal_service = MyService()

    rclpy.spin(minimal_service)

    minimal_service.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()