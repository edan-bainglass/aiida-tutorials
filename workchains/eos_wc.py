# -*- coding: utf-8 -*-
"""Equation of State WorkChain."""
from aiida.engine import ToContext, WorkChain, calcfunction
from aiida.orm import Code, Dict, Float, Str, StructureData, load_group
from aiida.plugins import CalculationFactory
from plumpy import WorkChainSpec
from rescale import rescale
from utils import generate_scf_input_params

PwCalculation = CalculationFactory("quantumespresso.pw")
scale_factors = (0.96, 0.98, 1.0, 1.02, 1.04)
labels = ["c1", "c2", "c3", "c4", "c5"]


@calcfunction
def get_eos_data(**kwargs):
    """Store EOS data in Dict node."""

    eos = [(
        result.dict.volume,
        result.dict.energy,
        result.dict.energy_units,
    ) for label, result in kwargs.items()]

    return Dict(dict={"eos": eos})


class EquationOfState(WorkChain):
    """WorkChain to compute Equation of State using Quantum ESPRESSO."""

    @classmethod
    def define(cls, spec: WorkChainSpec):
        """Specify inputs and outputs."""
        super().define(spec)

        spec.input("code", valid_type=Code)
        spec.input("pseudo_family_label", valid_type=Str)
        spec.input("structure", valid_type=StructureData)

        spec.output("result", valid_type=Dict)

        spec.outline(
            cls.run_eos,
            cls.results,
        )

    def run_eos(self):
        """Run calculations for equation of state."""
        structure = self.inputs.structure

        calculations = {}

        pseudo_family = load_group(self.inputs.pseudo_family_label.value)

        for label, factor in zip(labels, scale_factors):

            rescaled_structure = rescale(structure, Float(factor))

            inputs = generate_scf_input_params(
                rescaled_structure,
                self.inputs.code,
                pseudo_family,
            )

            self.report(
                f"Running an SCF calculation for {structure.get_formula()} with scale factor {factor}"
            )

            calcjob_node = self.submit(PwCalculation, **inputs)
            calculations[label] = calcjob_node

        return ToContext(**calculations)

    def results(self):
        """Process results."""

        inputs = {
            label: self.ctx[label] \
                .get_outgoing() \
                .get_node_by_label("output_parameters")
            for label in labels
        }
        eos = get_eos_data(**inputs)

        self.out("result", eos)
