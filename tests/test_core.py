# tests/test_core.py
from pyquerytracker.core import track_query

def test_tracking_output(capsys):
    @track_query
    def fake_db_query(): return "done"
    assert fake_db_query() == "done"
    captured = capsys.readouterr()
    assert "Function fake_db_query took" in captured.out
