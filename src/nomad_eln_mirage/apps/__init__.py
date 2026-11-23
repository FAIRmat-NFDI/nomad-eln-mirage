from nomad.config.models.plugins import AppEntryPoint
from nomad.config.models.ui import (
    App,
    Axis,
    AxisScale,
    Column,
    Dashboard,
    Layout,
    Menu,
    MenuItemHistogram,
    MenuItemPeriodicTable,
    MenuItemTerms,
    WidgetBoxPlot,
    WidgetHistogram,
    WidgetPeriodicTable,
    WidgetScatterPlot,
    WidgetTerms,
)

# Number of grid columns for each breakpoint, see WidgetGrid in nomad-gui.
_columns = {'sm': 12, 'md': 18, 'lg': 24, 'xl': 30, 'xxl': 36}


def _layout(
    index: int, row: int, column: int, per_row: int, height: int = 8
) -> dict[str, Layout]:
    """Grid placement for a widget. On the widest breakpoints the widget is put
    on the given row and column of a grid with `per_row` widgets per row. The
    `lg` breakpoint fills rows of two widgets in `index` order and narrower
    breakpoints stack all widgets in a single column."""
    layout = {}
    for breakpoint, n_columns in _columns.items():
        if breakpoint in ('xl', 'xxl'):
            width = n_columns // per_row
            x, y = column * width, row * height
        elif breakpoint == 'lg':
            width = n_columns // 2
            x, y = (index % 2) * width, (index // 2) * height
        else:
            width = n_columns
            x, y = 0, index * height
        layout[breakpoint] = Layout(x=x, y=y, w=width, h=height, minW=3, minH=3)
    return layout


eln_mirage_app = AppEntryPoint(
    name='ELN Mirage',
    description='App for testing the app features of the NOMAD GUI.',
    app=App(
        label='ELN Mirage',
        path='eln-mirage',
        category='Test',
        description='App for testing the app features of the NOMAD GUI.',
        columns=[
            Column(search_quantity='entry_name', title='Name', selected=True),
            Column(
                search_quantity='results.material.chemical_formula_hill',
                title='Formula',
                selected=True,
            ),
            Column(search_quantity='entry_type', selected=True),
            Column(search_quantity='upload_create_time', title='Upload time'),
        ],
        menu=Menu(
            items=[
                MenuItemPeriodicTable(search_quantity='results.material.elements'),
                MenuItemTerms(search_quantity='results.material.structural_type'),
                MenuItemHistogram(
                    x=Axis(search_quantity='results.material.n_elements')
                ),
            ]
        ),
        dashboard=Dashboard(
            widgets=[
                WidgetTerms(
                    type='terms',
                    title='Structural type',
                    search_quantity='results.material.structural_type',
                    layout=_layout(0, 0, 0, 3),
                ),
                WidgetHistogram(
                    type='histogram',
                    title='Number of elements',
                    x=Axis(search_quantity='results.material.n_elements'),
                    y=AxisScale(scale='linear'),
                    n_bins=30,
                    layout=_layout(1, 0, 1, 3),
                ),
                WidgetPeriodicTable(
                    type='periodic_table',
                    title='Elements',
                    search_quantity='results.material.elements',
                    layout=_layout(2, 0, 2, 3),
                ),
                WidgetScatterPlot(
                    type='scatter_plot',
                    title='Space group vs. elements',
                    x=Axis(search_quantity='results.material.n_elements'),
                    y=Axis(
                        search_quantity='results.material.symmetry.space_group_number'
                    ),
                    layout=_layout(3, 1, 0, 2),
                ),
                WidgetBoxPlot(
                    type='box_plot',
                    title='Space group distribution',
                    y=Axis(
                        search_quantity='results.material.symmetry.space_group_number'
                    ),
                    layout=_layout(4, 1, 1, 2),
                ),
            ]
        ),
    ),
)
