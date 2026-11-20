import os.path

import pytest
from nomad.client import normalize_all, parse


def get_archive(filename):
    test_file = os.path.join('tests', 'data', filename)
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)
    return entry_archive


@pytest.mark.parametrize(
    'filename,expected',
    [
        pytest.param(
            'plain_quantities.archive.yaml',
            {
                'plain_bool': True,
                'plain_int': 42,
                'plain_float': 6.28,
                'plain_str': 'peace',
            },
        ),
        pytest.param(
            'empty.archive.yaml',
            {
                'plain_bool': True,
                'plain_int': 12,
                'plain_float': 2.718,
                'plain_str': 'foobar',
            },
        ),
    ],
)
def test_plain_quantities(filename: str, expected: dict):
    entry_archive = get_archive(filename)
    data = getattr(entry_archive.data, 'plain_quantities')
    assert data is not None
    for key, expected_value in expected.items():
        assert getattr(data, key) == expected_value


@pytest.mark.parametrize(
    'filename,expected',
    [
        pytest.param(
            'edit_quantities.archive.yaml',
            {
                'edit_bool': True,
                'edit_number_int': 64,
                'edit_number_float': 1.23,
                'edit_str': 'rainbow',
                'edit_url': 'https://example.com/path/to/file',
                'edit_enum': 'Option 5',
                'edit_radio_enum': 'Green',
                'edit_slider': 7.0,
                'edit_autocomplete': 'Banana',
                'edit_rich_text': '<p>Hello rich text</p>',
                'edit_file': 'mirage.txt',
            },
        ),
    ],
)
def test_edit_quantities(filename: str, expected: dict):
    entry_archive = get_archive(filename)
    data = entry_archive.data
    for key, expected_value in expected.items():
        assert getattr(data, key) == expected_value


def test_statistics():
    entry_archive = get_archive('statistics.archive.yaml')
    data = entry_archive.data
    assert data.m_get_statistics('statistics_array') == pytest.approx(
        dict(mean=4, min=1, max=9, count=3)
    )
    # the normalizer sets the value and the statistics are computed afterwards
    assert data.normalized_array.shape == (2, 3, 4)
    assert data.m_get_statistics('normalized_array') == pytest.approx(
        dict(mean=11.5, std=(575 / 12) ** 0.5, min=0, max=23, count=24)
    )
