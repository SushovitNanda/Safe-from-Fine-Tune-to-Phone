import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts/mac'))
from deployment_stats import paired,retention,difference_in_differences


def test_matching_paired_vectors_and_difference_in_differences():
    a=np.ones(100);b=np.zeros(100)
    r=difference_in_differences(a,b,a,b,nboot=100)
    assert r['available'] and r['difference_pp']==0 and r['ci95_pp']==[0,0]
    assert not difference_in_differences(a,b,None,b)['available']
    assert paired(a,nboot=100)['p_boot']==.01
    with pytest.raises(ValueError):difference_in_differences(a,b,a[:-1],b)


def test_retention_floor_and_zero_denominator_are_not_silently_dropped():
    med=np.r_[np.ones(4),np.zeros(96)];rep=np.zeros(100)
    assert not retention(med,rep,med,rep,nboot=100)['available']
    med=np.r_[np.ones(5),np.zeros(95)]
    r=retention(med,rep,med,rep,nboot=1000)
    assert r['available'] and r['retention']==1
    assert r['bootstrap_denominator_below_5pp']>0
    assert r['bootstrap_denominator_nonpositive']>0 and r['ci95'] is None
    assert r['dropped_ratio_resamples']==r['bootstrap_denominator_nonpositive']


def test_stable_retention_has_full_paired_ratio_interval():
    med=np.ones(100);rep=np.zeros(100)
    r=retention(med,rep,med,rep,nboot=100)
    assert r['retention']==1 and r['ci95']==[1,1] and r['dropped_ratio_resamples']==0
