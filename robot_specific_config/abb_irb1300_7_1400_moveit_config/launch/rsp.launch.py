from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_rsp_launch


def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("abb_irb1300_7_1400", package_name="abb_irb1300_7_1400_moveit_config").to_moveit_configs()
    return generate_rsp_launch(moveit_config)
