import datetime
import os.path

from nomad.client import normalize_all, parse


def test_schema_package():
    test_file = os.path.join('tests', 'data', 'test.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    data = entry_archive.data
    assert data.bool_plain is True
    assert data.int_plain == 42  # noqa
    assert data.float_plain == 6.28  # noqa
    assert data.string_plain == 'peace'
    assert data.datetime_plain == datetime.datetime(
        2026, 4, 1, 12, 34, 56, tzinfo=datetime.timezone.utc
    )
