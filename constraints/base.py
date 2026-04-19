from abc import ABC, abstractmethod


class Constraint(ABC):
    """Base class for all scheduling constraints."""

    @abstractmethod
    def add(self, ctx):
        """Add this constraint to the solver via the context."""
        ...
