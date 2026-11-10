import re

import numpy as np
import pytest
from nomad.client import normalize_all, parse
from nomad.datamodel import EntryArchive, EntryMetadata
from plotly.graph_objects import Figure
from structlog import get_logger

from nomad_eln_mirage.schema_packages.eln_mirage import ELNMiragePlot

EXPECTED_PLOT_LABELS = [
    'Generated sine wave',
    'Scatter with color',
    'Bar chart',
    'Filled area',
    'Histogram',
    'Box plot',
    'Violin plot',
    'Heatmap',
    'Contour',
    'Express scatter',
    'Express multiple traces',
    'Annotated subplots',
    'Python Express line',
    'Python graph object scatter',
]


def assert_gallery_labels(data):
    assert [figure.label for figure in data.figures] == EXPECTED_PLOT_LABELS
    # Python figures embed the current samples, including after reprocessing.
    line, scatter = data.figures[-2:]
    np.testing.assert_allclose(line.figure['data'][0]['x'], data.x)
    np.testing.assert_allclose(line.figure['data'][0]['y'], data.signal)
    trace = scatter.figure['data'][0]
    np.testing.assert_allclose(trace['x'], data.x)
    np.testing.assert_allclose(trace['y'], data.cosine)
    assert trace['mode'] == 'markers'


def test_processing_generates_data_and_plot():
    archive = parse('tests/data/generated_plot.archive.yaml')[0]
    normalize_all(archive)
    data = archive.data

    np.testing.assert_allclose(data.x, np.linspace(0, 1, 201))
    np.testing.assert_allclose(data.signal, np.sin(4 * np.pi * data.x))
    assert_gallery_labels(data)
    trace = data.figures[0].figure['data']
    # Graph object references are resolved by the GUI against the processed archive.
    assert trace['x'] == '#x'
    assert trace['y'] == '#signal'
    resolved_trace = {
        **trace,
        'x': archive.m_resolve(f'{data.m_path()}/{trace["x"][1:]}'),
        'y': archive.m_resolve(f'{data.m_path()}/{trace["y"][1:]}'),
    }
    figure = Figure(data=[resolved_trace], layout=data.figures[0].figure['layout'])
    np.testing.assert_allclose(figure.data[0].x, data.x)
    np.testing.assert_allclose(figure.data[0].y, data.signal)

    # Saving changed inputs replaces both the generated samples and the figure.
    data.amplitude = 3.0
    data.cycles = 1.0
    data.number_of_points = 5
    normalize_all(archive)
    np.testing.assert_allclose(data.signal, [0, 3, 0, -3, 0], atol=1e-14)
    assert_gallery_labels(data)
    reference = data.figures[0].figure['data']['y']
    regenerated_signal = archive.m_resolve(f'{data.m_path()}/{reference[1:]}')
    np.testing.assert_allclose(regenerated_signal, data.signal)


def test_defaults_generate_a_plot():
    archive = EntryArchive(data=ELNMiragePlot(), metadata=EntryMetadata())
    normalize_all(archive)
    expected_points = 201
    assert len(archive.data.signal) == expected_points
    assert_gallery_labels(archive.data)


def test_reprocessing_saved_entry_with_twenty_points():
    archive = EntryArchive(data=ELNMiragePlot(), metadata=EntryMetadata())
    normalize_all(archive)

    # Simulate saving only a changed sample count on a previously processed entry.
    saved = archive.m_to_dict()
    saved['data']['number_of_points'] = 20
    reprocessed = EntryArchive.m_from_dict(saved)
    normalize_all(reprocessed)

    data = reprocessed.data
    expected_points = 20
    assert len(data.x) == len(data.signal) == expected_points
    np.testing.assert_allclose(data.x, np.linspace(0, 1, expected_points))
    np.testing.assert_allclose(data.signal, np.sin(4 * np.pi * data.x))
    assert_gallery_labels(data)
    figure = data.figures[0].figure
    assert figure['data']['mode'] == 'lines+markers'
    assert figure['layout']['title']['text'] == 'Generated sine wave'


@pytest.mark.parametrize('number_of_points', [2, 20, 201, 1000])
def test_all_gallery_figures_are_valid_plotly(number_of_points):
    archive = EntryArchive(
        data=ELNMiragePlot(number_of_points=number_of_points), metadata=EntryMetadata()
    )
    normalize_all(archive)
    data = archive.data
    assert_gallery_labels(data)

    def resolve(value):
        if isinstance(value, str) and value.startswith('#'):
            if re.fullmatch(r'#[0-9a-fA-F]{3}([0-9a-fA-F]{3})?', value):
                return value
            return archive.m_resolve(f'{data.m_path()}/{value[1:]}')
        if isinstance(value, dict):
            return {key: resolve(item) for key, item in value.items()}
        if isinstance(value, list):
            return [resolve(item) for item in value]
        return value

    for item in data.figures:
        payload = resolve(item.figure)
        # A single graph-object annotation produces a dict; the GUI wraps it.
        if isinstance(payload['data'], dict):
            payload['data'] = [payload['data']]
        figure = Figure(payload)
        assert figure.data, item.label
        allowed_types = {
            'scatter',
            'bar',
            'histogram',
            'box',
            'violin',
            'heatmap',
            'contour',
            'scatterpolar',
        }
        assert all(trace.type in allowed_types for trace in figure.data), item.label
        assert figure.to_json()

    expected_grid_size = min(number_of_points, 41)
    assert data.wave_grid.shape == (expected_grid_size, expected_grid_size)
    phase = 2 * np.pi * data.cycles * data.grid_axis
    np.testing.assert_allclose(
        data.wave_grid, data.amplitude * np.outer(np.sin(phase), np.cos(phase))
    )
    two_trace_plots = (
        'Express multiple traces',
        'Annotated subplots',
    )
    for item in data.figures:
        if item.label in two_trace_plots:
            expected_traces = 2
            assert len(item.figure['data']) == expected_traces
            np.testing.assert_allclose(item.figure['data'][0]['y'], data.signal)
            np.testing.assert_allclose(item.figure['data'][1]['y'], data.cosine)


@pytest.mark.parametrize(
    'parameters',
    [
        {'number_of_points': 1},
        {'number_of_points': 1001},
        {'amplitude': float('nan')},
        {'cycles': float('inf')},
    ],
)
def test_invalid_generation_parameters(parameters):
    archive = EntryArchive(data=ELNMiragePlot(**parameters))
    with pytest.raises(ValueError):
        archive.data.normalize(archive, get_logger())
