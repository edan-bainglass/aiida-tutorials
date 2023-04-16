from aiida.engine import ToContext, WorkChain
from aiida.orm import Code, Int
from aiida.plugins.factories import CalculationFactory
from plumpy import WorkChainSpec

ArithmeticAddCalculation = CalculationFactory("core.arithmetic.add")


class AddCalcjobWorkChain(WorkChain):
    """WorkChain to add two integers."""

    @classmethod
    def define(cls, spec: WorkChainSpec) -> None:
        """Specify inputs, outputs, and the workchain outline."""
        super().define(spec)

        spec.input("x", valid_type=Int)
        spec.input("y", valid_type=Int)
        spec.input("code", valid_type=Code)

        spec.outline(
            cls.add,
            cls.result,
        )

        spec.output("workchain_result", valid_type=Int)

    def add(self) -> None:
        """Sum the inputs."""
        calc_job_node = self.submit(
            ArithmeticAddCalculation,
            x=self.inputs.x,
            y=self.inputs.y,
            code=self.inputs.code,
        )
        # append `calc_job_node` as an awaitable
        return ToContext(add_node=calc_job_node)

    def result(self) -> None:
        """Parse the result."""
        self.out(
            "workchain_result",
            self.ctx.add_node.outputs.sum,
        )
