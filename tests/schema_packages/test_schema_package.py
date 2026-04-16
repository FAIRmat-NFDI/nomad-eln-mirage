import os.path

import pytest
from nomad.client import normalize_all, parse


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
                'plain_bool': False,
                'plain_int': 12,
                'plain_float': 2.718,
                'plain_str': 'foobar',
            },
        ),
    ],
)
def test_plain_quantities(filename: str, expected: dict):
    test_file = os.path.join('tests', 'data', filename)
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    data = getattr(entry_archive.data, 'plain_quantities')
    assert data is not None
    for key, expected_value in expected.items():
        assert getattr(data, key) == expected_value
