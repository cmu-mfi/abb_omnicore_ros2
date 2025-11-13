from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    LogInfo,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    LaunchConfiguration,
    PathJoinSubstitution,
    TextSubstitution,
)
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    declared_arguments = [
        DeclareLaunchArgument("sim", default_value="False", description="Simulation flag"),
        DeclareLaunchArgument(
            "robot_type",
            default_value="irb1300_7_140",
            description="Robot name, like irb1300_7_140 for IRB1300-7/1.40",
        ),
    ]

    sim_arg = LaunchConfiguration("sim")
    robot_type = LaunchConfiguration("robot_type")

    moveit_config_pkg = FindPackageShare(
        [TextSubstitution(text="abb_"), robot_type, TextSubstitution(text="_moveit_config")]
    )

    return LaunchDescription(declared_arguments + [
        # Optional: log the package name
        LogInfo(msg=["Using MoveIt config package: ", moveit_config_pkg]),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    moveit_config_pkg,
                    "launch",
                    "moveit.launch.py",
                ]),
            ]),
            launch_arguments={"sim": sim_arg}.items(),
        )
    ])
