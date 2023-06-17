"""Cop class implementation for Epstein paper
"""
import numpy as np
from entity import Entity


class Cop(Entity):
    def __init__(self, vision, x_0, y_0) -> None:
        """Cop constructor

        Args:
            vision (integer):
            x_0 (integer): initial x coordinate
            y_0 (integer): initial y coordinate
        """
        super().__init__(vision=vision, x=x_0, y=y_0)

    def action(self, grid):
        from agent import Agent

        fov = super().field_of_vision(grid)

        for element in fov:
            if element is None:
                continue
            elif isinstance(element, Agent) and element.active:
                grid.update_cell_value(element.x, element.y, None)

                break
