from aiida.engine import WorkChain, calcfunction
from aiida.orm import Int
from plumpy import WorkChainSpec


@calcfunction
def addition(x: Int, y: Int) -> Int:
    """Return the sum node of two integer nodes."""
    return x + y


@calcfunction
def multiplication(x: Int, y: Int) -> Int:
    """Return the product node of two integer nodes."""
    return x * y


class MultiplyAddWorkChain(WorkChain):
    """Workchain to multiply two integers and add a third."""

    @classmethod
    def define(cls, spec: WorkChainSpec) -> None:
        """Specify inputs, outputs, and the workchain outline."""
        super().define(spec)

        spec.input("x", valid_type=Int)
        spec.input("y", valid_type=Int)
        spec.input("z", valid_type=Int)
        spec.output("product", valid_type=Int)
        spec.output("sum", valid_type=Int)

        spec.outline(
            cls.multiply,
            cls.add,
            cls.result,
        )

    def multiply(self) -> None:
        """Multiply x and y."""
        self.ctx.product = multiplication(
            self.inputs.x,
            self.inputs.y,
        )

    def add(self) -> None:
        """Add z to the product of x and y."""
        self.ctx.sum = addition(
            self.ctx.product,
            self.inputs.z,
        )

    def result(self) -> None:
        """Parse the result."""
        self.out("product", self.ctx.product)
        self.out("sum", self.ctx.sum)
