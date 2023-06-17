import numpy as np


class Entity:
    def __init__(self, vision, x, y) -> None:
        self.vision = vision
        self.x = x
        self.y = y

    def move(self, grid):
        """Method that move agent to random empty square in his field of vision

        Args:
            grid (np.matrix): the grid in which the simulation is happening
        """

        possible_moves = []  # Will contain possible coordinates of empty squares

        for dx in range(-self.vision, self.vision + 1):
            for dy in range(-self.vision, self.vision + 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = self.x + dx, self.y + dy
                if (
                    0 <= nx < grid.grid_size
                    and 0 <= ny < grid.grid_size
                    and grid.get_cell_value(nx, ny) is None
                ):
                    possible_moves.append((nx, ny))

        # If there are not empty squares surrounding the agent it will
        # stand still
        if possible_moves:
            new_x, new_y = possible_moves[np.random.choice(len(possible_moves), 1)[0]]
            grid.update_cell_value(
                self.x, self.y, None
            )  # Remove agent from current cell

            grid.update_cell_value(new_x, new_y, self)  # Move agent to the new cell

            self.x = new_x
            self.y = new_y

    def action(self, grid):
        pass

    def field_of_vision(self, grid):
        """Method that computes what each agent sees in his field of vision
        Args:
            grid (np.matrix): the grid in which the simulation is taking place

        Returns:
            list: a list with the content of what the agent sees
        """
        fov = []

        for dx in range(-self.vision, self.vision + 1):
            for dy in range(-self.vision, self.vision + 1):
                nx, ny = self.x + dx, self.y + dy
                if (
                    0 <= nx < grid.grid_size
                    and 0 <= ny < grid.grid_size
                    and (dx != 0 or dy != 0)  # Exclude agent's own position
                ):
                    fov.append(grid.get_cell_value(nx, ny))

        return fov
