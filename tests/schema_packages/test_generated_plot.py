import numpy as np
import pytest
from nomad.client import normalize_all, parse
from nomad.datamodel import EntryArchive
from plotly.graph_objects import Figure
from structlog import get_logger

from nomad_eln_mirage.schema_packages.eln_mirage import ELNMiragePlot


def test_processing_generates_data_and_plot():
    archive = parse('tests/data/generated_plot.archive.yaml')[0]
    normalize_all(archive)
    data = archive.data

    np.testing.assert_allclose(data.x, np.linspace(0, 1, 201))
    np.testing.assert_allclose(data.signal, np.sin(4 * np.pi * data.x))
    assert len(data.figures) == 1
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
    assert len(data.figures) == 1
    reference = data.figures[0].figure['data']['y']
    regenerated_signal = archive.m_resolve(f'{data.m_path()}/{reference[1:]}')
    np.testing.assert_allclose(regenerated_signal, data.signal)


def test_defaults_generate_a_plot():
    archive = EntryArchive(data=ELNMiragePlot())
    normalize_all(archive)
    expected_points = 201
    assert len(archive.data.signal) == expected_points
    assert len(archive.data.figures) == 1


def test_reprocessing_saved_entry_with_twenty_points():
    archive = EntryArchive(data=ELNMiragePlot())
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
    assert len(data.figures) == 1
    figure = data.figures[0].figure
    assert figure['data']['mode'] == 'lines+markers'
    assert figure['layout']['title']['text'] == 'Generated sine wave (20 samples)'


@pytest.mark.parametrize(
    'parameters',
    [
        {'number_of_points': 1},
        {'number_of_points': 10001},
        {'amplitude': float('nan')},
        {'cycles': float('inf')},
    ],
)
def test_invalid_generation_parameters(parameters):
    archive = EntryArchive(data=ELNMiragePlot(**parameters))
    with pytest.raises(ValueError):
        archive.data.normalize(archive, get_logger())
