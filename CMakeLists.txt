cmake_minimum_required(VERSION 3.0.2)
project(pyvoyis_ros)
add_compile_options(-std=c++11)
find_package(catkin REQUIRED
  rospy
  message_generation
  message_runtime
)

# find_package(Boost REQUIRED COMPONENTS system)
catkin_python_setup()

# ###############################################
# # Declare ROS messages, services and actions ##
# ###############################################

# # Generate messages in the 'msg' folder
# add_message_files(
# FILES
# Message1.msg
# Message2.msg
# )

# # Generate services in the 'srv' folder
# add_service_files(
# FILES
# Service1.srv
# )

# # Generate actions in the 'action' folder
# add_action_files(
# FILES
# Action1.action
# Action2.action
# )

# # Generate added messages and services with any dependencies listed here
# generate_messages(
# DEPENDENCIES
# std_msgs  # Or other packages containing msgs
# )

# ###############################################
# # Declare ROS dynamic reconfigure parameters ##
# ###############################################

# # Generate dynamic reconfigure parameters in the 'cfg' folder
# generate_dynamic_reconfigure_options(
# cfg/DynReconf1.cfg
# cfg/DynReconf2.cfg
# )

# ##################################
# # catkin specific configuration ##
# ##################################
catkin_package(
  # INCLUDE_DIRS include
  # LIBRARIES pyvoyis_ros
  # CATKIN_DEPENDS other_catkin_pkg
  # DEPENDS system_lib
)

# ##########
# # Build ##
# ##########
include_directories(

  # include
  # ${catkin_INCLUDE_DIRS}
)

# add_library(${PROJECT_NAME}
# src/${PROJECT_NAME}/pyvoyis_ros.cpp
# )

# add_dependencies(${PROJECT_NAME} ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

# add_executable(${PROJECT_NAME}_node src/pyvoyis_ros_node.cpp)

# add_dependencies(${PROJECT_NAME}_node ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

# target_link_libraries(${PROJECT_NAME}_node
# ${catkin_LIBRARIES}
# )

# ############
# # Install ##
# ############
install(DIRECTORY config
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(DIRECTORY launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(DIRECTORY nodes
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

# ############
# # Testing ##
# ############
catkin_add_nosetests(test)
