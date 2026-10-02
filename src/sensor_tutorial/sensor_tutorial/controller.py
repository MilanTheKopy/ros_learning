import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan


class Controller(Node):

    def __init__(self):
        super().__init__('controller')

        self.get_logger().info(f'Controller created')
        self.lidar_subscription = self.create_subscription(
                    msg_type = LaserScan,
                    topic = '/lidar',
                    callback=self.lidar_callback,
                    qos_profile=10,
                    
                )


    def lidar_callback(self, msg):

        self.get_logger().info(f'Controller received lidar data. range_min: {msg.ranges[int(len(msg.ranges)/2)]}')


def main(args=None):
    rclpy.init(args=args)

    node = Controller()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()