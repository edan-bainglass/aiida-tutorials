from aiida.engine import WorkChain, calcfunction
from aiida.orm import Int


@calcfunction
def addition(x: Int, y: Int) -> Int:
    """Return the sum node of two integer nodes."""
    return x + y


class AddWorkChain(WorkChain):
    """Workchain to add two integers."""

    @classmethod
    def define(cls, spec):
        """Specify inputs, outputs, and the workchain outline."""
        super().define(spec)

        spec.input("x", valid_type=Int)
        spec.input("y", valid_type=Int)
        spec.output("workchain_result", valid_type=Int)

        spec.outline(
            cls.add,
            cls.result,
        )

    def add(self):
        """Sum the inputs."""
        addition_result = addition(self.inputs.x, self.inputs.y)
        self.ctx.summation = addition_result

    def result(self):
        """Parse the result."""
        self.out("workchain_result", self.ctx.summation)
