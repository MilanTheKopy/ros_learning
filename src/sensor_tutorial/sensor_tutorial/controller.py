import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

MIN_WALL_DISTANCE = 1
class Controller(Node):

    def __init__(self):
        super().__init__('controller')

        #self.get_logger().info(f'Controller created')
        self.lidar_subscription = self.create_subscription(
                    msg_type = LaserScan,
                    topic = '/lidar',
                    callback=self.lidar_callback,
                    qos_profile=10,
                    
                )
        self.twist_publisher = self.create_publisher(
                    Twist,
                    '/cmd_vel',
                    10
                )


    def lidar_callback(self, msg):
        front_range = msg.ranges[int(len(msg.ranges)/2)]
        right_side_range = msg.ranges[int(len(msg.ranges)/4)]
        #self.get_logger().info(f'Controller received lidar data. front_range: {front_range}, right_side_range: {right_side_range}')

        response = Twist()
        if min(front_range, right_side_range)<= MIN_WALL_DISTANCE:
            response.angular.z = 1.0
            response.linear.x = 0.0
        else:
            response.angular.z = 0.0
            response.linear.x = 1.0

        self.twist_publisher.publish(
            response
        )


def main(args=None):
    rclpy.init(args=args)

    node = Controller()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()