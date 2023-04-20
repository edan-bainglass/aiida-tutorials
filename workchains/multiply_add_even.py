from aiida.engine import ToContext, WorkChain, calcfunction
from aiida.orm import Bool, Code, Int
from multiply_add import MultiplyAddWorkChain
from plumpy import WorkChainSpec


@calcfunction
def check_if_even(value: Int) -> Bool:
    """Check if value is even."""
    return Bool(value % 2 == 0)


class MultiplyAddIsEvenWorkChain(WorkChain):
    """
    An extension of the MultiplyAddWorkChain that also
    checks if the result of MultiplyAddWorkChain is even.
    """

    @classmethod
    def define(cls, spec: WorkChainSpec) -> None:
        super().define(spec)

        spec.expose_inputs(MultiplyAddWorkChain, namespace='multi_add')

        spec.expose_outputs(MultiplyAddWorkChain)
        spec.output('is_even', valid_type=Bool)

        spec.outline(
            cls.multiply_add,
            cls.is_even,
        )

    def multiply_add(self) -> None:
        """Call MultiplyAddWorkChain."""
        multi_add_wc = self.submit(
            MultiplyAddWorkChain,
            **self.exposed_inputs(MultiplyAddWorkChain, 'multi_add'),
        )

        return ToContext(multi_add=multi_add_wc)

    def is_even(self) -> None:
        """Check if result is even."""
        is_even = check_if_even(self.ctx.multi_add.outputs.sum.value)

        self.out_many(
            self.exposed_outputs(
                self.ctx.multi_add,
                MultiplyAddWorkChain,
            ))

        self.out('is_even', is_even)
