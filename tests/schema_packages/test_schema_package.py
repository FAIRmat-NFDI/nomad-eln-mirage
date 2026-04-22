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
            },
        ),
    ],
)
def test_edit_quantities(filename: str, expected: dict):
    entry_archive = get_archive(filename)
    data = entry_archive.data
    for key, expected_value in expected.items():
        assert getattr(data, key) == expected_value
