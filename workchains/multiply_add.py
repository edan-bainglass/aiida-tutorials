from aiida.engine import ToContext, WorkChain, calcfunction
from aiida.orm import Code, Int
from aiida.plugins.factories import CalculationFactory
from plumpy import WorkChainSpec

ArithmeticAddCalculation = CalculationFactory("core.arithmetic.add")


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

        spec.input("code", valid_type=Code)
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
        inputs = {
            "code": self.inputs.code,
            "x": self.ctx.product,
            "y": self.inputs.z,
        }

        add_calc_job = self.submit(
            ArithmeticAddCalculation,
            **inputs,
        )

        return ToContext(add_node=add_calc_job)

    def result(self) -> None:
        """Parse the result."""
        self.out("product", self.ctx.product)
        self.out("sum", self.ctx.add_node.outputs.sum)
