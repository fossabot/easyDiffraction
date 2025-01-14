import pytest

from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QStandardItemModel

from PyImports.Calculators.CryspyCalculator import CryspyCalculator

import PyImports.Models.MeasuredDataModel as Model

TEST_FILE = "file:Tests/Data/main.cif"

def test_MeasuredDataModel():

    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)

    m = Model.MeasuredDataModel()
    m.setCalculator(calculator)


    assert isinstance(m._data_model, QStandardItemModel)
    assert isinstance(m._headers_model, QStandardItemModel)

    # assure _setModelFromProject got called
    assert m._data_model.rowCount() == 381
    assert m._data_model.columnCount() == 7

    assert m._headers_model.rowCount() == 1
    assert m._headers_model.columnCount() == 7

    # Test stuff from _setModelFromProject here
    assert m._data_model.item(0, 0).data(role=Qt.DisplayRole) == 4.0
    assert m._data_model.item(0, 6).data(role=Qt.DisplayRole) == 585.055382546602
    assert m._data_model.item(380, 0).data(role=Qt.DisplayRole) == 80.0
    assert m._data_model.item(380, 6).data(role=Qt.DisplayRole) == 762.9590461224967

    assert m._headers_model.item(0, 0).data(role=Qt.DisplayRole) == 'x'
    assert m._headers_model.item(0, 1).data(role=Qt.DisplayRole) == 'y_obs_up'
    assert m._headers_model.item(0, 2).data(role=Qt.DisplayRole) == 'sy_obs_up'
    assert m._headers_model.item(0, 3).data(role=Qt.DisplayRole) == 'y_obs_down'
    assert m._headers_model.item(0, 4).data(role=Qt.DisplayRole) == 'sy_obs_down'
    assert m._headers_model.item(0, 5).data(role=Qt.DisplayRole) == 'y_obs_upper'
    assert m._headers_model.item(0, 6).data(role=Qt.DisplayRole) == 'y_obs_lower'

    # test asModel
    assert m._data_model == m.asDataModel()
    assert m._headers_model == m.asHeadersModel()


def test_MeasuredDataModel_bad_calculator():

    calculator = None

    # null calculator
    with pytest.raises(AttributeError):
        m = Model.MeasuredDataModel()
        m.setCalculator(calculator)

    # empty file
    #file_path = QUrl("file:Tests/Data/empty.cif").toLocalFile()
    #with pytest.raises(IndexError):
    #    calculator = CryspyCalculator(file_path)
