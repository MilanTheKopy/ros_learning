from datetime import datetime

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist 


MIN_WALL_DISTANCE = 1
MAX_VEL= 6
MAX_SLOPE = 0.07
PID_SLOPE_BY_VEL = {
    "p": 1000,
    "i" : 0,
    "d": 20,
    "integrated_controlled_value_diff": 0,
    "last_controlled_value": 0
}
PID_VEL_BY_SLOPE = {
    "p": 0.00001,
    "i" : 0.00001,
    "d": 0.00001,
    "integrated_controlled_value_diff": 0,
    "last_controlled_value": 0
}

class Controller(Node):

    def __init__(self):
        super().__init__('controller')


        self.imu_subscription = self.create_subscription(
                    msg_type = Imu,
                    topic = '/imu',
                    callback=self.imu_callback,
                    qos_profile=10,
                    
                )
        self.odo_subscription = self.create_subscription(
                    msg_type = Odometry,
                    topic = '/odometry',
                    callback=self.odo_callback,
                    qos_profile=10,
                    
                )
        self.twist_publisher = self.create_publisher(
                    Twist,
                    '/cmd_vel',
                    10
        )

        self.last_control_loop = self.get_clock().now()
        self.cmd = Twist()
        self.odometry = Odometry()
    
        self.speed_setpoint = 0


    def odo_callback(self, msg):

        self.odometry = msg

    def imu_callback(self, msg):

        
        slope = msg.orientation.y
        now = self.get_clock().now()
        dt = (now  - self.last_control_loop).nanoseconds / 1e9
        self.last_control_loop = now
        interval = 60
        slope_setpoint = 0.04
        if now.nanoseconds / 1e9 % interval < interval/2:
            slope_setpoint = -0.04
   
            

        speed_setpoint= 0
        actual_vel = self.odometry.twist.twist.linear.x
        
        #slope_setpoint = self.pid_control(controlled_variable= actual_vel, setpoint=speed_setpoint, dt=dt, pid_params = PID_VEL_BY_SLOPE)
        #slope_setpoint = 0.02#min(MAX_SLOPE , max(-MAX_SLOPE , slope_setpoint)) 
        cmd_vel = self.pid_control(controlled_variable= slope, setpoint=slope_setpoint, dt=dt, pid_params = PID_SLOPE_BY_VEL)
        cmd_vel = float(min(MAX_VEL, max(-MAX_VEL, cmd_vel)))
        self.get_logger().info(f"actual_vel: {actual_vel}, speed_setpoint: {speed_setpoint}, slope_setpoint: {slope_setpoint}, slope: {slope}, dt: {dt}")
        self.cmd.linear.x = cmd_vel
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
        d= 0
        if dt >0:
            d = pid_params["d"] * dcontrol_variable/dt
        '''self.get_logger().info(
                    f'Controller publishing p: {p}, i: {i}, d: {d} for slope: {controlled_variable} with dt: {dt}'
                )'''
        return p + i + d


def main(args=None):
    rclpy.init(args=args)

    node = Controller()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()