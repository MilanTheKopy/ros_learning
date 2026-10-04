from datetime import datetime

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist

MIN_WALL_DISTANCE = 1
MAX_VEL= 6
MAX_SLOPE = 0.07
PID_SLOPE_BY_VEL = {
    "p": 20,
    "i" : 20,
    "d": 20,
    "integrated_controlled_value_diff": 0,
    "last_controlled_value": 0
}
PID_VEL_BY_SLOPE = {
    "p": 20,
    "i" : 20,
    "d": 20,
    "integrated_controlled_value_diff": 0,
    "last_controlled_value": 0
}

class Controller(Node):

    def __init__(self):
        super().__init__('controller')


        self.lidar_subscription = self.create_subscription(
                    msg_type = Imu,
                    topic = '/imu',
                    callback=self.imu_callback,
                    qos_profile=10,
                    
                )
        self.twist_publisher = self.create_publisher(
                    Twist,
                    '/cmd_vel',
                    10
        )

        self.last_control_loop = datetime.now()
        self.cmd = Twist()
        self.speed_setpoint = 0


  

    def imu_callback(self, msg):

        
        slope = msg.orientation.y
        now = datetime.now()
        dt = (now  - self.last_control_loop).total_seconds()
        self.last_control_loop = now
        interval = 120
        if now.second%interval < interval/2:
            self.speed_setpoint = 3
        else:
            self.speed_setpoint = -3


        self.slope_setpoint = self.pid_control(controlled_variable= self.cmd.linear.x, setpoint=self.speed_setpoint, dt=dt, pid_params = PID_VEL_BY_SLOPE)
        self.slope_setpoint = min(MAX_SLOPE , max(-MAX_SLOPE , self.slope_setpoint))
        cmd_vel = self.pid_control(controlled_variable= slope, setpoint=self.slope_setpoint, dt=dt, pid_params = PID_SLOPE_BY_VEL)
        
        self.cmd.linear.x = float(min(MAX_VEL, max(-MAX_VEL, cmd_vel)))
        self.twist_publisher.publish(
                            self.cmd
                        )

    def pid_control(self, controlled_variable: float, setpoint: float, dt:int, pid_params:dict):

        diff = controlled_variable - setpoint
        pid_params["integrated_controlled_value_diff"] += diff * dt
        dcontrol_variable = controlled_variable - pid_params["last_controlled_value"]
        pid_params["last_controlled_value"]= controlled_variable

        p = pid_params["p"] * diff
        i = pid_params["i"] * pid_params["integrated_controlled_value_diff"]
        d = pid_params["d"] * dcontrol_variable/dt
        self.get_logger().info(
                    f'Controller publishing p: {p}, i: {i}, d: {d} for slope: {controlled_variable} with dt: {dt}'
                )
        return p + i + d


def main(args=None):
    rclpy.init(args=args)

    node = Controller()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()