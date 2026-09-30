cmake_minimum_required(VERSION 3.8)
project(interfaces_package)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Measurement.msg"
  "srv/CoolnessTest.srv"
)

ament_package()