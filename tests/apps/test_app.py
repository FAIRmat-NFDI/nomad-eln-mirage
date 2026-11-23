from nomad.config.models.ui import App


def test_app_entry_point():
    from nomad_eln_mirage.apps import eln_mirage_app

    app = App.model_validate(eln_mirage_app.app.model_dump())
    assert app.path == 'eln-mirage'
    widget_types = [widget.type for widget in app.dashboard.widgets]
    assert widget_types == [
        'terms',
        'histogram',
        'periodic_table',
        'scatter_plot',
        'box_plot',
    ]
    titles = [widget.title for widget in app.dashboard.widgets]
    assert len(set(titles)) == len(titles)
