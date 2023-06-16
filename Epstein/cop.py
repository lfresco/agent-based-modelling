"""Cop class implementation for Epstein paper
"""
import numpy as np
from entity import Entity


class Cop(Entity):
    def __init__(self, vision, x_0, y_0) -> None:
        """Cop constructor

        Args:
            vision (integer):
            x_0 (_type_): _description_
            y_0 (_type_): _description_
        """
        super().__init__(vision=vision, x=x_0, y=y_0)
