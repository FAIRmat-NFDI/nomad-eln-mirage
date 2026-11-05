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


import numpy as np
from nomad.datamodel.data import Author, EntryData, User
from nomad.datamodel.hdf5 import HDF5Reference
from nomad.datamodel.metainfo.basesections import BaseSection
from nomad.datamodel.metainfo.plot import PlotSection
from nomad.metainfo import (
    Datetime,
    MEnum,
    Package,
    Quantity,
    Reference,
    Section,
    SubSection,
)

m_package = Package(name='ELN Mirage')

MIN_PLOT_POINTS = 2
MAX_PLOT_POINTS = 1000
MAX_GRID_POINTS = 41


class ELNMiragePlainQuantities(EntryData):
    m_def = Section()

    plain_bool = Quantity(type=bool, description='Plain boolean', default=True)
    plain_int = Quantity(type=int, description='Plain integer', default=12)
    plain_float = Quantity(type=float, description='Plain float', default=2.718)
    plain_str = Quantity(type=str, description='Plain string', default='foobar')


class ELNMirageLabeledSection(EntryData):
    m_def = Section(label_quantity='title')

    title = Quantity(
        type=str,
        description='Label shown by section references',
        a_eln={'component': 'StringEditQuantity'},
    )


class ELNMirageNamedSection(BaseSection, EntryData):
    """
    Has no label quantity, the label falls back to the name inherited from BaseSection.
    """

    m_def = Section()


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
    edit_required = Quantity(
        type=str,
        required=True,
        description='Edit required string',
        a_eln={'component': 'StringEditQuantity'},
    )
    edit_required_eln = Quantity(
        type=str,
        description='Edit required string from ELN annotation',
        a_eln={'component': 'StringEditQuantity', 'required': True},
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
    edit_autocomplete = Quantity(
        type=MEnum('Apple', 'Banana', 'Cherry', 'Date', 'Elderberry'),
        description='Edit autocomplete',
        a_eln={'component': 'AutocompleteEditQuantity'},
    )
    edit_datetime = Quantity(
        type=Datetime,
        description='Edit datetime',
        a_eln={'component': 'DateTimeEditQuantity'},
    )
    edit_rich_text = Quantity(
        type=str,
        description='Edit rich text',
        a_eln={'component': 'RichTextEditQuantity'},
    )
    edit_reference = Quantity(
        type=Reference(ELNMiragePlainQuantities.m_def),
        description='Edit reference',
        a_eln={'component': 'ReferenceEditQuantity'},
    )
    edit_section_label_reference = Quantity(
        type=Reference(ELNMirageLabeledSection.m_def),
        description='Edit reference that shows the section label',
        a_eln={'component': 'ReferenceEditQuantity', 'showSectionLabel': True},
    )
    edit_entry_data_reference = Quantity(
        type=Reference(EntryData.m_def),
        description='Edit reference to any entry that shows the section label',
        a_eln={'component': 'ReferenceEditQuantity', 'showSectionLabel': True},
    )
    edit_file = Quantity(
        type=str,
        description='Edit file',
        a_eln={'component': 'FileEditQuantity'},
    )
    edit_hdf5_reference = Quantity(
        # HDF5Reference quantities are editable in the gui without an eln annotation.
        type=HDF5Reference,
        description='Edit HDF5 reference',
    )
    edit_user = Quantity(
        type=User,
        description='Edit user',
        a_eln={'component': 'AuthorEditQuantity'},
    )
    edit_author = Quantity(
        type=Author,
        description='Edit author',
        a_eln={'component': 'AuthorEditQuantity'},
    )


class ELNMiragePlot(PlotSection, EntryData):
    """Generate a gallery demonstrating Python-defined plots during processing."""

    m_def = Section(
        label='ELN Mirage Plot',
        a_plotly_graph_object=[
            {
                'label': 'Generated sine wave',
                'open': True,
                'data': {
                    'type': 'scatter',
                    'mode': 'lines+markers',
                    'x': '#x',
                    'y': '#signal',
                },
                'layout': {
                    'title': {'text': 'Generated sine wave'},
                    'xaxis': {'title': {'text': 'Normalized position'}},
                    'yaxis': {'title': {'text': 'Signal'}},
                },
            },
            {
                'label': 'Scatter with color',
                'data': {
                    'type': 'scatter',
                    'mode': 'markers',
                    'x': '#x',
                    'y': '#signal',
                    'marker': {
                        'color': '#cosine',
                        'colorscale': 'Viridis',
                        'showscale': True,
                    },
                },
            },
            {
                'label': 'Bar chart',
                'data': {'type': 'bar', 'x': '#x', 'y': '#signal'},
            },
            {
                'label': 'Filled area',
                'data': {
                    'type': 'scatter',
                    'mode': 'lines',
                    'x': '#x',
                    'y': '#signal',
                    'fill': 'tozeroy',
                },
            },
            {
                'label': 'Histogram',
                'data': {'type': 'histogram', 'x': '#signal', 'nbinsx': 20},
            },
            {
                'label': 'Box plot',
                'data': {'type': 'box', 'y': '#signal', 'boxpoints': 'all'},
            },
            {
                'label': 'Violin plot',
                'data': {
                    'type': 'violin',
                    'y': '#signal',
                    'box': {'visible': True},
                    'points': 'all',
                },
            },
            {
                'label': 'Heatmap',
                'data': {
                    'type': 'heatmap',
                    'x': '#grid_axis',
                    'y': '#grid_axis',
                    'z': '#wave_grid',
                    'colorscale': 'Viridis',
                },
            },
            {
                'label': 'Contour',
                'data': {
                    'type': 'contour',
                    'x': '#grid_axis',
                    'y': '#grid_axis',
                    'z': '#wave_grid',
                    'colorscale': 'Viridis',
                },
            },
        ],
        a_plotly_express=[
            {
                'label': 'Express scatter',
                'method': 'scatter',
                'x': '#x',
                'y': '#signal',
                'color': '#cosine',
            },
            {
                'label': 'Express multiple traces',
                'method': 'line',
                'x': '#x',
                'y': '#signal',
                'traces': [{'method': 'line', 'x': '#x', 'y': '#cosine'}],
            },
        ],
        a_plotly_subplots=[
            {
                'label': 'Annotated subplots',
                'parameters': {'rows': 1, 'cols': 2},
                'plotly_express': [
                    {'method': 'line', 'x': '#x', 'y': '#signal'},
                    {'method': 'scatter', 'x': '#x', 'y': '#cosine'},
                ],
            },
        ],
    )

    amplitude = Quantity(
        type=float,
        default=1.0,
        description='Amplitude of the generated sine wave.',
        a_eln={'component': 'NumberEditQuantity'},
    )
    cycles = Quantity(
        type=float,
        default=2.0,
        description='Number of sine wave cycles across the plotted interval.',
        a_eln={'component': 'NumberEditQuantity'},
    )
    number_of_points = Quantity(
        type=int,
        default=201,
        description='Number of generated samples, from 2 to 1000.',
        a_eln={
            'component': 'NumberEditQuantity',
            'minValue': MIN_PLOT_POINTS,
            'maxValue': MAX_PLOT_POINTS,
        },
    )
    x = Quantity(
        type=np.float64,
        shape=['*'],
        description='Generated positions from 0 to 1, regenerated during processing.',
    )
    signal = Quantity(
        type=np.float64,
        shape=['*'],
        description='Generated amplitude * sin(2 * pi * cycles * x).',
    )
    cosine = Quantity(
        type=np.float64,
        shape=['*'],
        description='Generated amplitude * cos(2 * pi * cycles * x).',
    )
    grid_axis = Quantity(
        type=np.float64,
        shape=['*'],
        description='Positions for matrix plots, capped at 41 samples per axis.',
    )
    wave_grid = Quantity(
        type=np.float64,
        shape=['*', '*'],
        description='Generated 2D sine/cosine product for heatmap and contour.',
    )

    def normalize(self, archive, logger):
        if not MIN_PLOT_POINTS <= self.number_of_points <= MAX_PLOT_POINTS:
            raise ValueError('number_of_points must be between 2 and 1000')
        if not np.isfinite(self.amplitude) or not np.isfinite(self.cycles):
            raise ValueError('amplitude and cycles must be finite')

        self.x = np.linspace(0.0, 1.0, self.number_of_points)
        self.signal = self.amplitude * np.sin(2 * np.pi * self.cycles * self.x)
        self.cosine = self.amplitude * np.cos(2 * np.pi * self.cycles * self.x)
        self.grid_axis = np.linspace(
            0.0, 1.0, min(self.number_of_points, MAX_GRID_POINTS)
        )
        phase = 2 * np.pi * self.cycles * self.grid_axis
        self.wave_grid = self.amplitude * np.outer(np.sin(phase), np.cos(phase))

        # Generate the figure after updating the referenced arrays.
        super().normalize(archive, logger)


m_package.__init_metainfo__()
