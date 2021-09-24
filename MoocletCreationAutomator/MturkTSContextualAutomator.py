from MoocletCreationAutomator.utils import parse_regression_formuala, create_coefficient_covariance_and_mean_matrix
from MoocletCreationAutomator.MoocletConnector import MoocletConnector
import json

class MturkTSContextualAutomator:
    def __init__(self, arms_no, policy_ids, round_no):
        self.arms_no = arms_no
        self.policy_ids = policy_ids
        self.mooclet = MoocletConnector()
        self.round_no = round_no

    def create_mooclet_object(self):
        params = {
            "policy": self.policy_ids[0],
            "name": f"MTurk TS Survey Round {self.round_no}",
        }
        id = self.mooclet.create_mooclet_object(params)
        return id

    def create_versions_object(self, mooclet_id):
        for arm_no, value in self.arms_no.items():
            name = f"MTurk TS Survey Arm {arm_no} Round {self.round_no}"
            params = {
                "mooclet": mooclet_id,
                "name": name,
                "text": f"arm {arm_no}",
                "version_json": json.dumps({f"is_arm{list(self.arms_no.keys())[0]}_round_{self.round_no}": value})
            }
            self.mooclet.create_version_object(params)
        return f"is_arm{list(self.arms_no.keys())[0]}_round_{self.round_no}"

    def create_policy_parameters(self, mooclet_id, policy_dict):
        for policy, info in policy_dict.items():
            params = {
                "mooclet": mooclet_id,
                "policy": info["id"],
                "parameters": json.dumps(info["params"])
            }
            self.mooclet.create_policy_parameter(params)

    def create_variables(self, reward, contextuals):
        self.mooclet.create_variable({"name": reward})
        for contextual in contextuals:
            self.mooclet.create_variable({"name": contextual})
        self.mooclet.create_variable({
            "name": f"Mooclet: MTurk TS Survey Round {self.round_no}_choose_policy_group"
        })

    def _construct_choose_policy_group_dict(self, ur, ts_c):
        return {
            "id": 12,
            "params":{
                "policy_options":
                    {
                        "uniform_random":ur,
                        "thompson_sampling_contextual": ts_c
                    }
            }
        }

    def _construct_ts_contextual_dict(self, regression_formula, arm_json, contextuals, batch_size):
        reward, length = parse_regression_formuala(regression_formula)
        cov, mean = create_coefficient_covariance_and_mean_matrix(length)
        action_space = {}
        action_space[arm_json] = [0, 1]
        params = {
            "coef_cov": cov,
            "coef_mean": mean,
            "batch_size": batch_size,
            "variance_a": 2,
            "variance_b": 1,
            "action_space": action_space,
            "include_intercept": 1,
            "outcome_variable": reward,
            "regression_formula": regression_formula,
            "contextual_variables": contextuals + ["version"],
            "precesion_draw": 1,
            "coef_draw": 1
        }
        return {
            "id": 6,
            "params": params
        }

    def construct_policy_param_dict(self, regression_formula, arm_json, contextuals, batch_size, ur, ts_c):
        return {
            "choose_policy_group": self._construct_choose_policy_group_dict(ur, ts_c),
            "ts_contextual": self._construct_ts_contextual_dict(regression_formula, arm_json, contextuals, batch_size)
        }

    def __call__(self, regression_formula, contextuals, batch_size=3, ur=0.0, ts_c=1.0):
        mooclet_id = self.create_mooclet_object()
        if not mooclet_id:
            return None
        arm_json = self.create_versions_object(mooclet_id)
        policy_parameters = self.construct_policy_param_dict(
            regression_formula=regression_formula,
            arm_json=arm_json,
            contextuals=contextuals,
            batch_size=batch_size,
            ur=ur,
            ts_c=ts_c
        )
        self.create_policy_parameters(mooclet_id, policy_parameters)
        reward, _ = parse_regression_formuala(formula, include_intercept=True)
        self.create_variables(reward, contextuals)


if __name__ == "__main__":
    # round number for MOOClet (make sure you are adding the new round of MOOClet)
    round_no = 32

    # 12 - choose policy group, 6 - ts contextual
    policy_ids = [12, 6]

    # suppose it is study comparing arm 5 vs arm 6, and you want to set the version variable to arm5=1 and arm6=0
    arms_no = {5: 1, 6: 0}

    # contextuals variables
    contextuals = []
    # contextuals = [f"mood_round_{round_no}", f"energy_round_{round_no}"]

    # regression formula
    # NOTE: do not include BETA, INTERCEPT in the formula
    # formula = {
    #     "reward_variable": ,
    #     "In":
    # }
    formula = f"mturk_ts_reward_round_{round_no} ~ is_arm{list(arms_no.keys())[0]}_round_{round_no}"

    # batch_size
    # batch_size = 5
    automator = MturkTSContextualAutomator(arms_no, policy_ids, round_no)
    automator(formula, contextuals)






