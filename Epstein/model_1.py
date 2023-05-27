import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


class Agent:
    def __init__(self, hardship, legitimacy, risk_aversion, vision, x_0, y_0) -> None:
        self.hardship = hardship
        self.legitimacy = legitimacy
        self.grievance = hardship * (1 - legitimacy)
        self.risk_aversion = risk_aversion
        self.vision = vision
        self.x = x_0
        self.y = y_0
        self.active = False

    def field_of_vision(self, grid):
        fov = []
        for dx in range(-self.vision, self.vision + 1):
            for dy in range(-self.vision, self.vision + 1):
                nx, ny = self.x + dx, self.y + dy
                if (
                    0 <= nx < grid.shape[0]
                    and 0 <= ny < grid.shape[1]
                    and (dx != 0 or dy != 0)  # Exclude agent's own position
                ):
                    fov.append(grid[nx, ny])

        return fov


class Cop:
    def __init__(self, vision, x_0, y_0) -> None:
        self.vision = vision
        self.x = x_0
        self.y = y_0


class Grid:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = np.empty((grid_size, grid_size), dtype=object)


class Model:
    def __init__(
        self, n_agents, n_cops, grid_size, legitimacy, agent_vision, cop_vision
    ):
        self.agents = []
        self.cops = []
        self.grid_size = grid_size
        self.legitimacy = legitimacy
        self.agent_vision = agent_vision
        self.cop_vision = cop_vision
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
                x_0=x,
                y_0=y,
            )

            self.grid[x, y] = agent
            self.agents.append((agent, x, y))

    def get_random_empty_location(self):
        while True:
            x = np.random.randint(0, self.grid_size)
            y = np.random.randint(0, self.grid_size)
            if self.grid[x, y] is None:
                return x, y

    def run(self, n_steps):
        conflict_history = []

        cmap = mcolors.ListedColormap(["sandybrown", "blue", "red", "black"])
        bounds = [0, 1, 2, 3, 4]
        norm = mcolors.BoundaryNorm(bounds, cmap.N)
        plt.figure()

        for step in range(n_steps):
            plt.imshow(
                [
                    [self.get_plot_color(x, y) for y in range(self.grid_size)]
                    for x in range(self.grid_size)
                ],
                cmap=cmap,
                norm=norm,
                origin="lower",
                extent=[0, self.grid_size, 0, self.grid_size],
            )
            plt.title(f"Step {step+1}")
            plt.xlabel("X", fontsize=10)
            plt.ylabel("Y", fontsize=10)
            plt.xticks(range(self.grid_size + 1), fontsize=8)
            plt.yticks(range(self.grid_size + 1), fontsize=8)
            plt.grid(color="white", linewidth=1)

            plt.show()

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
    model = Model(20, 5, 40, 0.5, 1, 1)
    model.run(10)
