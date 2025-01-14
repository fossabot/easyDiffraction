import logging

from PySide2.QtCore import Qt, QObject, Signal
from PySide2.QtGui import QStandardItemModel

class CalculatedDataModel(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._headers_model = QStandardItemModel()
        self._data_model = QStandardItemModel()
        self._project_dict = None

    def _setModelsFromProjectDict(self):
        """Create the model needed for GUI calculated data table and chart."""
        logging.info("+++++++++++++++++++++++++ setData start") # profiling
        for experiment_id, experiment_dict in self._project_dict['calculations'].items():
            self._data_model.blockSignals(True)
            self._headers_model.blockSignals(True)
            #
            column_count = len(experiment_dict['calculated_pattern'].items())
            row_count = len(list(experiment_dict['calculated_pattern'].items())[0][1])
            self._data_model.setColumnCount(column_count)
            self._data_model.setRowCount(row_count)
            #
            for colum_index, (data_id, data_list) in enumerate(experiment_dict['calculated_pattern'].items()):
                index = self._headers_model.index(0, colum_index)
                self._headers_model.setData(index, data_id, Qt.DisplayRole)
                for row_index, value in enumerate(data_list):
                    index = self._data_model.index(row_index, colum_index)
                    self._data_model.setData(index, value, Qt.DisplayRole)
            #
            self._data_model.blockSignals(False)
            self._headers_model.blockSignals(False)
            self._data_model.layoutChanged.emit()
            self._headers_model.layoutChanged.emit()
        logging.info("+++++++++++++++++++++++++ setData end") # profiling

    def onProjectChanged(self):
        """Set headers and data models from project dictionary"""
        self._setModelsFromProjectDict()

    def asHeadersModel(self):
        """Return headers model."""
        return self._headers_model

    def asDataModel(self):
        """Return data model."""
        return self._data_model

    def setCalculator(self, calculator):
        calculator.projectDictChanged.connect(self.onProjectChanged)
        self._project_dict = calculator.asDict()
        self._setModelsFromProjectDict()
