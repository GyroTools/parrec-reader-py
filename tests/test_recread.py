import pytest
from parrec.recread import Recread


def test_read_par():
    rec = Recread('./data/rf_12102012_1332440_1_1_wipsurveyV42.par')

    assert rec.parfile == './data/rf_12102012_1332440_1_1_wipsurveyV42.par'
    assert rec.recfile == './data/rf_12102012_1332440_1_1_wipsurveyV42.rec'

    data = rec.read()
    assert data.shape == (256, 256, 60)

def test_read_rec():
    rec = Recread('./data/rf_12102012_1332440_1_1_wipsurveyV42.rec')

    assert rec.parfile == './data/rf_12102012_1332440_1_1_wipsurveyV42.par'
    assert rec.recfile == './data/rf_12102012_1332440_1_1_wipsurveyV42.rec'

    data = rec.read()
    assert data.shape == (256, 256, 60)

def test_read_image():
    rec = Recread('./data/rf_12102012_1332440_1_1_wipsurveyV42.rec')

    assert rec.parfile == './data/rf_12102012_1332440_1_1_wipsurveyV42.par'
    assert rec.recfile == './data/rf_12102012_1332440_1_1_wipsurveyV42.rec'

    with pytest.raises(ValueError) as e:
        data = rec.read_image(80)

    data = rec.read_image(10)
    assert data.shape == (256, 256)
