from causal_world.intervention_actors.base_actor import \
    BaseInterventionActorPolicy
import numpy as np


class CurriculumInterventionActorPolicy(BaseInterventionActorPolicy):

    def __init__(self, **kwargs):
        """
        This is a random intervention actor which intervenes randomly on
        all available state variables except joint positions since its a
        trickier space.

        :param kwargs:
        """
        super(CurriculumInterventionActorPolicy, self).__init__()
        self.task_intervention_space = None
        self.random = 1

    def initialize(self, env, ratio):
        """
        This functions allows the intervention actor to query things from the env, such
        as intervention spaces or to have access to sampling funcs for goals..etc

        :param env: (causal_world.env.CausalWorld) the environment used for the
                                                   intervention actor to query
                                                   different methods from it.

        :return:
        """
        self.task_intervention_space = env.get_variable_space_used()
        return

    def _act(self, variables_dict, ratio):
        """

        :param variables_dict:
        :return:
        """
        #choose randomly to intervene on size OR cylindrical position since
        #size affects cylindrical position
        interventions_dict = dict()
        for variable in self.task_intervention_space:
            if isinstance(self.task_intervention_space[variable], dict):
                interventions_dict[variable] = dict()
                for subvariable_name in self.task_intervention_space[variable]:

                    interventions_dict[variable][subvariable_name] =\
                        np.random.uniform(
                        self.task_intervention_space[variable][subvariable_name][0],
                        self.task_intervention_space[variable][subvariable_name][1] * ratio + (1 - ratio) * self.task_intervention_space[variable][subvariable_name][0])
                    # interventions_dict[variable][subvariable_name] =\
                    #     np.random.uniform(
                    #     self.task_intervention_space
                    #     [variable][subvariable_name][0],
                    #     self.task_intervention_space
                    #     [variable][subvariable_name][1])
            else:
                interventions_dict[variable] = np.random.uniform(
                    self.task_intervention_space[variable][0],
                    self.task_intervention_space[variable][1] * self.ratio + (1 - self.ratio) * self.task_intervention_space[variable][0])
        return interventions_dict

    def get_params(self):
        """
        returns parameters that could be used in recreating this intervention
        actor.

        :return: (dict) specifying paramters to create this intervention actor
                        again.
        """
        return {'curriculum_actor': dict()}
