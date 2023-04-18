from aiida.engine import calcfunction
from aiida.orm import Float, StructureData


@calcfunction
def rescale(structure: StructureData, scale: Float):
    """Calculation function to rescale a structure

    :param structure: An AiiDA `StructureData` to rescale
    :param scale: The scale factor (for the lattice constant)
    :return: The rescaled structure
    """

    ase_structure = structure.get_ase()
    scale_value = scale.value

    new_cell = ase_structure.get_cell() * scale_value
    ase_structure.set_cell(new_cell, scale_atoms=True)

    return StructureData(ase=ase_structure)
