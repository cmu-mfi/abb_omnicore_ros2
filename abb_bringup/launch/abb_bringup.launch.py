import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    IncludeLaunchDescription,
)
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    LaunchConfiguration,
    PathJoinSubstitution,
    TextSubstitution,
)


def generate_launch_description():
    
    # 1. read command line arguments
    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
            "sim", default_value="False", description="Simulation flag",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "robot_ip", default_value="", description="Robot IP address",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "launch_rviz", default_value="True", description="Launch RViz",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "robot_type", default_value="irb1300_7_140", description="Robot name, like irb1300_7_140 for IRB1300-7/1.40",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "robot_class",
            default_value="irb1300",
            description="Robot class, like irb1300 for IRB1300",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "namespace", default_value="", description="Robot namespace",
        )
    )

    sim = LaunchConfiguration("sim")
    robot_ip = LaunchConfiguration("robot_ip")
    launch_rviz = LaunchConfiguration("launch_rviz")
    robot_type = LaunchConfiguration("robot_type")
    robot_class = LaunchConfiguration("robot_class")
    
    launch_controller = os.path.join(
        get_package_share_directory("abb_bringup"),
        "launch",
        "abb_control.launch.py",
    )
    launch_moveit = os.path.join(
        get_package_share_directory("abb_bringup"),
        "launch",
        "abb_moveit.launch.py",
    )
    
    include_controller = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(launch_controller),
        launch_arguments={
            "description_package": [
                TextSubstitution(text="abb_"),
                robot_class,
                TextSubstitution(text="_support"),
            ],
            # "description_file": "irb1300_7_140.xacro",
            "description_file": [
                robot_type,
                TextSubstitution(text=".xacro"),
            ],
            "launch_rviz": launch_rviz,
            "use_fake_hardware": "false",
            "rws_ip": robot_ip,
            "rws_port": "443",
        }.items(),
        condition=UnlessCondition(sim),
    )
    include_moveit = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(launch_moveit),
        launch_arguments={
            "sim": sim,
            "robot_type": robot_type,
            "launch_rviz": launch_rviz,
        }.items(),
    )
    

    return LaunchDescription([
        *declared_arguments,
        include_controller,
        include_moveit
    ])