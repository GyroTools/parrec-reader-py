import pytest

from parrec.parread import Parread


def test_read_upper_parameters():
    par = Parread('./data/rf_12102012_1332440_1_1_wipsurveyV42.par')
    with open(par.parfile) as file:
        upper_pars = par._read_upper_part(file)

    assert len(upper_pars) == 35
    assert upper_pars['ExaminationName'] == 'rfr test2'
    assert upper_pars['ScanDuration'] == 23.11
    assert upper_pars['AcquisitionNr'] == 1
    assert upper_pars['ScanResolution'] == [192, 96]
    assert upper_pars['Fov'] == [450.00, 200.00, 450.00]
    assert upper_pars['WaterFatShift'] == 0.97
    assert upper_pars['NumberOfLabelTypes'] == 0


def test_get_definitions():
    par = Parread('./data/rf_12102012_1332440_1_1_wipsurveyV42.par')
    with open(par.parfile) as file:
        definitions = par._get_information_pars_definition(file)

    assert len(definitions) == 41
    assert definitions[0] == ('SliceNumber', 1, 1)
    assert definitions[9] == ('ReconResolution', 1, 2)
    assert definitions[10] == ('RescaleIntercept', 2, 1)
    assert definitions[15] == ('ImageAngulation', 2, 3)
    assert definitions[38] == ('DiffusionAnisotropyType', 3, 1)


def test_read_lower_parameters():
    par = Parread('./data/rf_12102012_1332440_1_1_wipsurveyV42.par')
    with open(par.parfile) as file:
        lower_pars = par._read_lower_part(file)

    assert len(lower_pars) == 60
    assert lower_pars[0]['SliceNumber'] == 1
    assert lower_pars[1]['SliceNumber'] == 2
    assert lower_pars[2]['SliceNumber'] == 3
    assert lower_pars[0]['ReconResolution'] == [256, 256]
    assert lower_pars[0]['RescaleSlope'] == 1.2862
    assert lower_pars[0]['ImageOffcentre'] == [-0.000, -95.000,  -0.000]
    assert lower_pars[59]['ImageOffcentre'] == [-0.000, 0.000, -142.500]
    assert lower_pars[10]['ImageFlipAngle'] == 20.0


def test_read():
    par = Parread('./data/rf_12102012_1332440_1_1_wipsurveyV42.par')
    pars = par.read()

    assert len(pars) == 36
    assert 'ImageInformation' in pars
    assert len(pars['ImageInformation']) > 0






