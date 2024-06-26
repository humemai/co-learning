from matrx.logger.logger import GridWorldLogger
from matrx.grid_world import GridWorld


class ActionLogger(GridWorldLogger):

    def __init__(self, save_path="", file_name_prefix="", file_extension=".csv", delimiter=";"):
        super().__init__(save_path=save_path, file_name=file_name_prefix, file_extension=file_extension,
                         delimiter=delimiter, log_strategy=1)

    def log(self, grid_world, agent_data):
        log_data = {}
        for agent_id, agent_body in grid_world.registered_agents.items():
            if 'human_selector' in agent_id or 'robot' in agent_id:
                log_data[agent_id + '_action'] = agent_body.current_action
                #log_data[agent_id + '_action_result'] = None
                #if agent_body.action_result is not None:
                #    log_data[agent_id + '_action_result'] = agent_body.action_result.succeeded
                log_data[agent_id + '_location'] = agent_body.location
                if 'robot' in agent_id:
                    log_data[agent_id + '_executing_cp'] = agent_body.properties['executing_cp']

        return log_data
