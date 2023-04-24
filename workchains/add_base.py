from typing import Optional
from aiida.engine import BaseRestartWorkChain, ExitCode, ProcessHandlerReport, process_handler, while_
from aiida.orm import Int, ProcessNode
from aiida.plugins import CalculationFactory
from plumpy import WorkChainSpec

ArithmeticAddCalculation = CalculationFactory('core.arithmetic.add')


class ArithmeticAddBaseWorkChain(BaseRestartWorkChain):
    """Base class for arithmetic addition with restart functionality."""

    _process_class = ArithmeticAddCalculation

    @classmethod
    def define(cls, spec: WorkChainSpec) -> None:
        super().define(spec)

        spec.expose_inputs(
            ArithmeticAddCalculation,
            namespace='add',
        )

        spec.expose_outputs(ArithmeticAddCalculation)

        spec.outline(
            cls.setup,
            while_(cls.should_run_process)(
                cls.run_process,
                cls.inspect_process,
            ),
            cls.results,
        )

    def setup(self) -> None:
        """Call the `setup` of the `BaseRestartWorkChain` and then create the
        inputs dictionary in `self.ctx.inputs`.

        This `self.ctx.inputs` dictionary will be used by the
        `BaseRestartWorkChain` to submit the process in the internal loop.
        """
        super().setup()

        self.ctx.inputs = self.exposed_inputs(
            ArithmeticAddCalculation,
            'add',
        )

    @process_handler(
        priority=400,
        exit_codes=ArithmeticAddCalculation.exit_codes.ERROR_NEGATIVE_NUMBER,
    )
    def handle_negative_sum(self, node):
        """If sum is negative, apply absolute value to both operands.

        param node:
            the node of the subprocess that was ran in the current iteration.
        :return: optional :class: `ProcessHandlerReport` instance to signal
            that a problem was detected and potentially handled.
        """
        self.ctx.inputs['x'] = Int(abs(node.inputs.x.value))
        self.ctx.inputs['y'] = Int(abs(node.inputs.y.value))
        return ProcessHandlerReport(do_break=True)

        # # example of refusal to handle an error
        # return ProcessHandlerReport( \
        #     exit_code=ExitCode(
        #         450,
        #         'Inputs lead to a negative sum but I will not correct them',
        #     ))
