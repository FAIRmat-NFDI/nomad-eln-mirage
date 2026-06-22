#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from nomad.datamodel.data import EntryData
from nomad.metainfo import MEnum, Package, Quantity, Section, SubSection

m_package = Package(name='ELN Mirage')


class ELNMiragePlainQuantities(EntryData):
    m_def = Section()

    plain_bool = Quantity(type=bool, description='Plain boolean', default=True)
    plain_int = Quantity(type=int, description='Plain integer', default=12)
    plain_float = Quantity(type=float, description='Plain float', default=2.718)
    plain_str = Quantity(type=str, description='Plain string', default='foobar')


class ELNMirage(EntryData):
    """
    ELN Mirage
    """

    m_def = Section()

    plain_quantities = SubSection(section_def=ELNMiragePlainQuantities)

    edit_bool = Quantity(
        type=bool, description='Edit boolean', a_eln={'component': 'BoolEditQuantity'}
    )
    edit_number_int = Quantity(
        type=int,
        description='Edit integer number',
        a_eln={'component': 'NumberEditQuantity'},
    )
    edit_number_float = Quantity(
        type=float,
        description='Edit float number',
        a_eln={'component': 'NumberEditQuantity'},
    )
    edit_number_with_shape = Quantity(
        type=int,
        shape=['*'],
        description='Edit number with shape',
        a_eln={'component': 'NumberEditQuantity'},
    )
    edit_number_with_unit = Quantity(
        type=float,
        unit='m',
        description='Edit number with unit',
        a_eln={'component': 'NumberEditQuantity'},
    )
    edit_str = Quantity(
        type=str, description='Edit string', a_eln={'component': 'StringEditQuantity'}
    )
    edit_url = Quantity(
        type=str, description='Edit URL', a_eln={'component': 'URLEditQuantity'}
    )
    edit_enum = Quantity(
        # More than 8 options so the gui renders a select/combobox rather than radios.
        type=MEnum(
            'Option 1',
            'Option 2',
            'Option 3',
            'Option 4',
            'Option 5',
            'Option 6',
            'Option 7',
            'Option 8',
            'Option 9',
        ),
        description='Edit enum',
        a_eln={'component': 'EnumEditQuantity'},
    )
    edit_radio_enum = Quantity(
        type=MEnum('Red', 'Green', 'Blue'),
        description='Edit radio enum',
        a_eln={'component': 'RadioEnumEditQuantity'},
    )
    edit_slider = Quantity(
        type=float,
        description='Edit slider',
        a_eln={'component': 'SliderEditQuantity', 'minValue': 0, 'maxValue': 10},
    )

m_package.__init_metainfo__()
