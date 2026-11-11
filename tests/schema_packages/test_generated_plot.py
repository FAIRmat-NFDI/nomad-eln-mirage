import numpy as np
from nomad.client import normalize_all, parse
from nomad.datamodel import EntryArchive, EntryMetadata

from nomad_eln_mirage.schema_packages.eln_mirage import ELNMiragePlot

EXPECTED_PLOT_LABELS = [
    'Python Express line',
    'Python graph object scatter',
]


def assert_generated_figures(data):
    assert [figure.label for figure in data.figures] == EXPECTED_PLOT_LABELS
    # Python figures embed the current samples, including after reprocessing.
    line, scatter = data.figures
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
    assert_generated_figures(data)


def test_reprocessing_saved_entry_updates_figures():
    archive = EntryArchive(data=ELNMiragePlot(), metadata=EntryMetadata())
    normalize_all(archive)

    # Reprocess saved figures after changing the generation parameters.
    saved = archive.m_to_dict()
    saved['data']['number_of_points'] = 20
    saved['data']['amplitude'] = 3.0
    saved['data']['cycles'] = 1.0
    reprocessed = EntryArchive.m_from_dict(saved)
    normalize_all(reprocessed)

    data = reprocessed.data
    expected_points = 20
    assert len(data.x) == len(data.signal) == expected_points
    np.testing.assert_allclose(data.x, np.linspace(0, 1, expected_points))
    np.testing.assert_allclose(data.signal, 3 * np.sin(2 * np.pi * data.x))
    assert_generated_figures(data)
    figure = data.figures[0].figure
    assert figure['data'][0]['mode'] == 'lines+markers'
    assert figure['layout']['title']['text'] == 'Python Plotly Express line'
