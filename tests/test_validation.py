def test_trivial_correlation():
    import numpy as np
    from mymodule import detection_statistic
    A = np.ones(100)
    B = -A
    r, p, z = detection_statistic(A, B)
    assert r < -0.9
