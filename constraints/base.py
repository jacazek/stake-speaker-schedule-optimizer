from abc import ABC, abstractmethod


class Constraint(ABC):
    """Base class for all scheduling constraints."""

    def __init__(self, ctx):
        self.ctx = ctx

    @abstractmethod
    def add(self, solver):
        """Add this constraint to the solver."""
        ...
