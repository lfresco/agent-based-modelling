import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from agent import Agent
from cop import Cop
from typing import Union


class Grid:
    def __init__(self, grid_size: int) -> None:
        """Constructor of grid

        Args:
            grid_size (integer): size of one side of the matrix
        """
        self.grid_size = grid_size
        self.grid = np.empty((grid_size, grid_size), dtype=object)
        self.grid.fill(None)

    def update_cell_value(
        self, x: int, y: int, content: Union[None, Agent, Cop]
    ) -> None:
        """Function that updates content of a given cell

        Args:
            x (integer): x coordinate of grid cell
            y (integer): y coordinate of grid cell
            content (object): the object that will be contained in the cell
        """
        self.grid[x, y] = content

    def get_number_of_active_agents(self):
        agents = [
            element
            for row in self.grid
            for element in row
            if isinstance(element, Agent) and element.active
        ]
        return len([element for element in agents if element.active])

    def get_number_of_agents(self):
        return len(
            [
                element
                for row in self.grid
                for element in row
                if isinstance(element, Agent)
            ]
        )

    def get_number_of_cops(self):
        return len(
            [
                element
                for row in self.grid
                for element in row
                if isinstance(element, Cop)
            ]
        )

    def get_agents_and_cops(self):
        agents = []
        cops = []

        agents = [
            element
            for row in self.grid
            for element in row
            if isinstance(element, Agent)
        ]
        cops = [
            element for row in self.grid for element in row if isinstance(element, Cop)
        ]

        return agents, cops

    def get_cell_value(self, x: int, y: int) -> Union[None, Agent, Cop]:
        """Returns content of a certain cell

        Args:
            x (integer): x coordinate of grid cell
            y (integer): y coordinate of grid cell

        Returns:
            Union[None, Agent, Cop]: the content of the cell
        """
        return self.grid[x, y]

    def get_random_empty_location(self):
        """Function that returns the coordinates of an empty cell in the grid

        Returns:
            Tuple(int, int): coordinates of empty grid cell
        """
        while True:
            x = np.random.randint(0, self.grid_size)
            y = np.random.randint(0, self.grid_size)
            if self.grid[x, y] is None:
                return x, y

    def get_plot_colors(self, x: int, y: int, plot_type="entities"):
        """Helper function that assignes correct color to each grid cell.


        Args:
            x (integer): x coordinate of grid cell
            y (integer): y coordinate of grid cell
            plot_type (str, optional): the type of plot we want to make. Defaults to "entities".

        Returns:
            integer: the
        """

        if self.grid[x, y] is None:
            return 0
        elif isinstance(self.grid[x, y], Cop):
            return 1
        elif isinstance(self.grid[x, y], Agent):
            if plot_type == "entities":
                agent = self.grid[x, y]
                if agent.active:
                    return 3
                else:
                    return 2
            else:
                hardship = self.grid[x, y].hardship
            return 2 + int(hardship * (self.cmap.N - 2))

    def plot(self, plot_type="entities"):
        """Methods that allows us to plot the current state of the grid.
           To mimic the plots showed in the paper it has two different
           modalities:
           - "entites" : which plots cops in black and agents in blue if quiet, red if active
           - "aggrevation" : which plots cops in black and the the level of hardship
                             endured by the agents

        Args:
            plot_type (str, optional): the type of plot we are interested in. Defaults to "entities".
        """

        self.cmap = (
            mcolors.ListedColormap(
                [
                    "sandybrown",
                    "black",
                    "blue",
                    "red",
                ]
            )
            if plot_type == "entities"
            else mcolors.ListedColormap(["sandybrown", "black", "red"])
        )
        bounds = [0, 1, 2, 3, 4] if plot_type == "entities" else [0, 1, 2, 3]

        norm = mcolors.BoundaryNorm(bounds, self.cmap.N)
        plt.figure()
        fig, ax = plt.subplots()

        grid_image = ax.imshow(
            [
                [self.get_plot_colors(x, y) for y in range(self.grid_size)]
                for x in range(self.grid_size)
            ],
            cmap=self.cmap,
            norm=norm,
            origin="lower",
            extent=[0, self.grid_size, 0, self.grid_size],
        )
        text_active = ax.text(
            -0.5,
            -0.0,
            "",
            horizontalalignment="center",
            verticalalignment="center",
            transform=ax.transAxes,
        )
        text_active.set_text(
            f"Total Active Agents: {np.sum(np.vectorize(lambda x: isinstance(x, Agent))(self.grid))}"
        )

        plt.title("Social Conflict Model")
        plt.xlabel("X", fontsize=10)
        plt.ylabel("Y", fontsize=10)
        plt.xticks(range(self.grid_size + 1), fontsize=8)
        plt.yticks(range(self.grid_size + 1), fontsize=8)
        plt.grid(color="white", linewidth=1)

        plt.show(block=False)
        plt.pause(0.5)
        plt.close()
