import os
import pytest

from parrec.xmlread import Xmlread

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
XML_FILE = os.path.join(DATA_DIR, 'T2W_TSE_SimpleRecon.xml')
REC_FILE = os.path.join(DATA_DIR, 'T2W_TSE_SimpleRecon.rec')


def test_read_series_info():
    xml = Xmlread(XML_FILE)
    import xml.etree.ElementTree as ET
    root = ET.parse(xml.xmlfile).getroot()
    series = xml._read_series_info(root)

    assert len(series) == 44
    assert series['ExaminationName'] == 'T2W_TSE'
    assert series['Technique'] == 'SE'
    assert series['ScanMode'] == 'MS'
    assert series['MaxNoSlices'] == 3
    assert series['ScanDuration'] == 0.0
    assert series['ScanResolutionX'] == 480
    assert series['RepetitionTimes'] == [3000.0, 0.0]
    assert series['PhaseEncodingVelocity'] == [0.0, 0.0, 0.0]
    assert series['FovAp'] == pytest.approx(200.976)
    assert series['FovFh'] == pytest.approx(48.0)
    assert series['OffCenterAp'] == pytest.approx(-12.3536)
    assert series['OffCenterFh'] == pytest.approx(-0.6012)


def test_read_image_array():
    xml = Xmlread(XML_FILE)
    import xml.etree.ElementTree as ET
    root = ET.parse(xml.xmlfile).getroot()
    images = xml._read_image_array(root)

    assert len(images) == 3
    assert len(images[0]) == 50

    assert images[0]['Slice'] == 2
    assert images[1]['Slice'] == 3
    assert images[2]['Slice'] == 1

    assert images[0]['Index'] == 0
    assert images[1]['Index'] == 1
    assert images[2]['Index'] == 2

    assert images[0]['EchoTime'] == pytest.approx(80.0)
    assert images[0]['RescaleSlope'] == pytest.approx(1.425641)
    assert images[0]['ScaleSlope'] == pytest.approx(0.1571324)
    assert images[0]['SliceGap'] == pytest.approx(18.0)
    assert images[0]['PixelSpacing'] == [pytest.approx(0.4187), pytest.approx(0.4187)]
    assert images[0]['SliceOrientation'] == 'Transversal'
    assert images[0]['ContrastType'] == 'T2'
    assert images[0]['ResolutionX'] == 480
    assert images[0]['ResolutionY'] == 480

    assert images[0]['OffcenterFh'] == pytest.approx(-0.6012)
    assert images[1]['OffcenterFh'] == pytest.approx(21.3988)
    assert images[2]['OffcenterFh'] == pytest.approx(-22.6012)


def test_read():
    xml = Xmlread(XML_FILE)
    pars = xml.read()

    assert len(pars) == 45
    assert 'ImageInformation' in pars
    assert len(pars['ImageInformation']) == 3


def test_get_xmlfile():
    xmlfile = Xmlread.get_xmlfile(REC_FILE)
    assert xmlfile == XML_FILE

    xmlfile = Xmlread.get_xmlfile(XML_FILE)
    assert xmlfile == XML_FILE
