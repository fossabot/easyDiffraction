import logging

from PySide2.QtCore import Qt, QObject, Signal, Slot, Property
from PySide2.QtGui import QStandardItem, QStandardItemModel

import PyImports.Helpers as Helpers

class AtomAdpsModel(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._project_dict = None
        self._model = QStandardItemModel()
        # set roles
        self._label_role = Qt.UserRole + 1
        self._type_role = Qt.UserRole + 2
        self._uiso_role = Qt.UserRole + 3
        self._u11_role = Qt.UserRole + 4
        self._u22_role = Qt.UserRole + 5
        self._u33_role = Qt.UserRole + 6
        self._u12_role = Qt.UserRole + 7
        self._u13_role = Qt.UserRole + 8
        self._u23_role = Qt.UserRole + 9
        self._model.setItemRoleNames({
            self._label_role: b'label',
            self._type_role: b'type',
            self._uiso_role: b'uiso',
            self._u11_role: b'u11',
            self._u22_role: b'u22',
            self._u33_role: b'u33',
            self._u12_role: b'u12',
            self._u13_role: b'u13',
            self._u23_role: b'u23'
            })

    def _setModelFromProject(self):
        """Create the model needed for GUI ..."""
        logging.info("+++++++++++++++++++++++++ setData start") # profiling
        for phase_id, phase_dict in self._project_dict['phases'].items():
            # block model signals
            self._model.blockSignals(True)
            # set list of atoms
            data = []
            for atom_id, atom_dict in phase_dict['atom_site'].items():
                data.append({
                    self._label_role: atom_id,
                    self._type_role: Helpers.nested_get(atom_dict, ['adp_type', 'value']),
                    self._uiso_role: Helpers.nested_get(atom_dict, ['B_iso_or_equiv', 'value']),
                    self._u11_role: Helpers.nested_get(atom_dict, ['u_11', 'value']),
                    self._u22_role: Helpers.nested_get(atom_dict, ['u_22', 'value']),
                    self._u33_role: Helpers.nested_get(atom_dict, ['u_33', 'value']),
                    self._u12_role: Helpers.nested_get(atom_dict, ['u_12', 'value']),
                    self._u13_role: Helpers.nested_get(atom_dict, ['u_13', 'value']),
                    self._u23_role: Helpers.nested_get(atom_dict, ['u_23', 'value']),
                    })
            # set model size
            self._model.setColumnCount(1)
            self._model.setRowCount(len(data))
            # set model from data list created above
            for row_index, dict in enumerate(data):
                index = self._model.index(row_index, 0)
                for role, value in dict.items():
                    self._model.setData(index, value, role)
            # unblock signals and emit model layout changed
            self._model.blockSignals(False)
            self._model.layoutChanged.emit()
        logging.info("+++++++++++++++++++++++++ setData end") # profiling

    def onProjectChanged(self):
        """Define what to do if project dict is changed, e.g. by external library object."""
        self._setModelFromProject()

    def asModel(self):
        """Return model."""
        return self._model

    def setCalculator(self, calculator):
        calculator.projectDictChanged.connect(self.onProjectChanged)
        self._project_dict = calculator.asDict()
        self._setModelFromProject()