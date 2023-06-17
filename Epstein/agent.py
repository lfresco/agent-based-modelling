import math
import numpy as np
from entity import Entity


class Agent(Entity):
    def __init__(
        self, hardship, legitimacy, risk_aversion, vision, threshold, x, y, k
    ) -> None:
        """Agent class constructor

        Args:
            hardship (double): agent’s perceived hardship
            legitimacy (double): the perceived legitimacy of the regim
            risk_aversion (double): agent’s level of risk aversion
            vision (integer): agent’s vision. This is the numberof lattice positions that the agent is able to inspect.
            threshold (double): threshold at which agent switches state between active/quiet
            x_0 (integer): x coordinate of initial position
            y_0 (integer): y coordinate of initial position
            k (double): constant set to ensure a plausible estimate of probability
        """
        super().__init__(vision=vision, x=x, y=y)
        self.hardship = hardship
        self.legitimacy = legitimacy
        self.grievance = hardship * (1 - legitimacy)
        self.risk_aversion = risk_aversion
        self.vision = vision
        self.threshold = threshold
        self.active = False
        self.k = k

    def action(self, grid):
        from cop import Cop

        """Method that at each iteration determinates if the agent
           will activate or not

        Args:
            grid (np.matrix): the grid in which the simulation is happening
        """

        fov = self.field_of_vision(grid)
        n_cops = 0
        n_agents = 1  # Each agent counts itself as a possible active one

        for element in fov:
            if element is None:
                continue
            elif isinstance(element, Cop):
                n_cops += 1
            else:
                if element.active:
                    n_agents += 1

        c_a_v = n_cops / n_agents  # Ratio between number of cops and number of agents

        P = 1 - math.exp((self.k * c_a_v))  # Estimated probability of being arrested

        N = P * self.risk_aversion  # Agent's net risk

        # Agent's behavioral rule
        if (self.grievance - N) > self.threshold:
            self.active = True
        elif (self.grievance - N) <= self.threshold:
            self.active = False
