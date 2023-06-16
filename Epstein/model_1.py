import random
from agent import Agent
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from cop import Cop


class Grid:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = np.empty((grid_size, grid_size), dtype=object)


class Model:
    def __init__(
        self,
        n_agents,
        n_cops,
        grid_size,
        legitimacy,
        agent_vision,
        cop_vision,
        threshold,
        k,
    ):
        self.agents = []
        self.cops = []
        self.grid_size = grid_size
        self.legitimacy = legitimacy
        self.agent_vision = agent_vision
        self.cop_vision = cop_vision
        self.k = k
        self.threshold = threshold
        self.grid = np.empty((grid_size, grid_size), dtype=object)
        self.grid.fill(None)

        self.initialize_agents(n_agents)
        self.initialize_cops(n_cops)

    def initialize_cops(self, n_cops):
        for _ in range(n_cops):
            x, y = self.get_random_empty_location()
            cop = Cop(self.cop_vision, x, y)
            self.grid[x, y] = cop
            self.cops.append((cop, x, y))

    def initialize_agents(self, n_agents):
        for _ in range(n_agents):
            hardship = np.random.uniform()

            risk_aversion = np.random.uniform()
            x, y = self.get_random_empty_location()
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

            self.grid[x, y] = agent
            self.agents.append((agent, x, y))

    def get_random_empty_location(self):
        while True:
            x = np.random.randint(0, self.grid_size)
            y = np.random.randint(0, self.grid_size)
            if self.grid[x, y] is None:
                return x, y

    def step(self):
        self.agents_and_cops = self.agents + self.cops

        random.shuffle(self.agents + self.cops)

        # Iterate through all agents and cops
        for entity, _, _ in self.agents + self.cops:
            # Move the entity
            entity.move(self.grid)
            if isinstance(entity, Agent):
                entity.action(self.grid)

    def run(self, n_steps):
        conflict_history = []

        cmap = mcolors.ListedColormap(["sandybrown", "blue", "red", "black"])
        bounds = [0, 1, 2, 3, 4]
        norm = mcolors.BoundaryNorm(bounds, cmap.N)
        plt.figure()
        fig, ax = plt.subplots()

        grid_image = ax.imshow(
            [
                [self.get_plot_color(x, y) for y in range(self.grid_size)]
                for x in range(self.grid_size)
            ],
            cmap=cmap,
            norm=norm,
            origin="lower",
            extent=[0, self.grid_size, 0, self.grid_size],
        )
        text_active = ax.text(
            0.5,
            -0.1,
            "",
            horizontalalignment="center",
            verticalalignment="center",
            transform=ax.transAxes,
        )
        text_activated = ax.text(
            0.5,
            -0.15,
            "",
            horizontalalignment="center",
            verticalalignment="center",
            transform=ax.transAxes,
        )

        plt.title("Social Conflict Model")
        plt.xlabel("X", fontsize=10)
        plt.ylabel("Y", fontsize=10)
        plt.xticks(range(self.grid_size + 1), fontsize=8)
        plt.yticks(range(self.grid_size + 1), fontsize=8)
        plt.grid(color="white", linewidth=1)

        plt.show(block=False)

        for step in range(n_steps):
            active_agents_before = sum(1 for agent, _, _ in self.agents if agent.active)
            self.step()
            active_agents_after = sum(1 for agent, _, _ in self.agents if agent.active)
            grid_image.set_array(
                [
                    [self.get_plot_color(x, y) for y in range(self.grid_size)]
                    for x in range(self.grid_size)
                ]
            )
            text_active.set_text(f"Total Active Agents: {active_agents_before}")
            text_activated.set_text(
                f"Activated Agents: {active_agents_after - active_agents_before}"
            )

            plt.pause(0.1)

        # plt.show()

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
    model = Model(70, 10, 40, 0.9, 1, 1, 0.1, 2.3)
    model.run(30)
