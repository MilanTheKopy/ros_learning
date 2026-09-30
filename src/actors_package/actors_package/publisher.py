import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from interfaces_package.msg import Measurement


class MyPublisher(Node):

    def __init__(self):
        super().__init__('my_publisher')

        self.publisher = self.create_publisher(
            Measurement,
            'my_topic',
            10
        )

        self.timer = self.create_timer(
            1.0,
            self.timer_callback
        )

        self.counter = 0

    def timer_callback(self):
        msg = Measurement()
        msg.unit = 'm'
        msg.value = 12.0

        self.publisher.publish(msg)

        self.get_logger().info(
            f'Publishing: "{str(msg)}"'
        )

        self.counter += 1


def main(args=None):
    rclpy.init(args=args)

    node = MyPublisher()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()