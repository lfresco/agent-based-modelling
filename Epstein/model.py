import random
from agent import Agent
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from cop import Cop
from grid import Grid
import time


class Model:
    def __init__(
        self,
        pop_density,
        cop_density,
        grid_size,
        legitimacy,
        agent_vision,
        cop_vision,
        threshold,
        k,
    ):
        """Constructor for Model class

        Args:
            pop_density (double): specifies the density of the agents following Epstein's implementation
            cop_density (double): specifies cop density wrt the grid size
            grid_size (integer): the size of the grid
            legitimacy (_type_): percievied legitimacy of the regime by the agents
            agent_vision (_type_): number of squares the agent can see
            cop_vision (_type_): number of squares the cop can see
            threshold (_type_): the threshold at which agents activate or go quiet
            k (_type_): constant that help in computing probability
        """
        self.agents = []
        self.cops = []
        self.grid_size = grid_size
        self.legitimacy = legitimacy
        self.agent_vision = agent_vision
        self.cop_vision = cop_vision
        self.k = k
        self.threshold = threshold
        self.n_agents = int(pop_density * (grid_size * grid_size))
        self.n_cops = int(cop_density * (grid_size * grid_size))
        self.grid = Grid(grid_size)

        self.initialize_agents(self.n_agents)
        self.initialize_cops(self.n_cops)

    def initialize_cops(self, n_cops: int) -> None:
        """Function that takes an integer representing the number of cops and
           randomely places them inside the grid

        Args:
            n_cops (integer): the number of cops that will be used in the model
        """
        for _ in range(n_cops):
            x, y = self.grid.get_random_empty_location()
            cop = Cop(self.cop_vision, x, y)
            self.grid.update_cell_value(x, y, cop)

            self.cops.append((cop, x, y))

    def initialize_agents(self, n_agents: int) -> None:
        """Function that takes an integer representing the number of cops and
           randomely places them inside the grid

        Args:
            n_cops (integer): the number of cops that will be used in the model
        """
        for _ in range(n_agents):
            hardship = np.random.uniform()

            risk_aversion = np.random.uniform()
            x, y = self.grid.get_random_empty_location()
            agent = Agent(
                hardship=hardship,
                legitimacy=self.legitimacy,
                risk_aversion=risk_aversion,
                vision=self.agent_vision,
                x=x,
                y=y,
                threshold=self.threshold,
                k=self.k,
            )

            self.grid.update_cell_value(x, y, agent)
            self.agents.append((agent, x, y))

    def step(self):
        self.agents, self.cops = self.grid.get_agents_and_cops()
        agents_and_cops = self.agents + self.cops
        random.shuffle(agents_and_cops)

        # Iterate through all agents and cops
        for entity in agents_and_cops:
            # Move the entity
            entity.move(self.grid)
            entity.action(self.grid)

    def run(self, n_steps):
        conflict_history = []

        for step in range(n_steps):
            self.step()

            self.grid.plot()

            print(f"Number of cops : {self.grid.get_number_of_cops()}")
            print(
                f"Number of active agents : {self.grid.get_number_of_active_agents()}"
            )
            print(f"Number of agents : {self.grid.get_number_of_agents()}")
            print("##################################")

        return conflict_history

    def get_plot_color(self, x, y):
        if self.grid[x, y] is None:
            return 0
        elif isinstance(self.grid[x, y], Agent):
            agent = self.grid[x, y]
            if agent.active:
                return 2
            else:
                return 1
        elif isinstance(self.grid[x, y], Cop):
            return 3


if __name__ == "__main__":
    grid_size = 40
    pop_density = 0.9

    cop_density = 0.01

    model = Model(
        pop_density=pop_density,
        cop_density=cop_density,
        grid_size=grid_size,
        legitimacy=0.9,
        cop_vision=1,
        agent_vision=7,
        threshold=0.1,
        k=2.3,
    )
    model.run(30)
