from pathlib import Path
import sys
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts/mac'))
import run_rq6_cells


def test_rq6_publisher_uses_its_actual_public_output_directory(monkeypatch,tmp_path):
    calls=[]
    monkeypatch.setattr(run_rq6_cells,'ROOT',tmp_path)
    monkeypatch.setattr(run_rq6_cells,'PUBLIC',tmp_path/'results/mac/nov11')
    monkeypatch.setattr(run_rq6_cells.subprocess,'check_output',lambda *a,**k:'manishshaw-nov9\n')
    def run(cmd,**kw):
        calls.append(cmd);return SimpleNamespace(returncode=0)
    monkeypatch.setattr(run_rq6_cells.subprocess,'run',run)
    run_rq6_cells.publish({'completed_cells':{},'status':'generating'})
    assert ['git','add','--','results/mac/nov11'] in calls
    assert ['git','push','origin','HEAD:manishshaw-nov9'] in calls
