from PyQt5.QtWidgets import QDialog

from dialogs.mi_options_ui import Ui_MiOptionsDialog
from utils import trycatchslot


class MiOptionsDialog(QDialog):
    def __init__(self, sampling_interval, queue_size, discard_oldest, filter, datachange_trigger, deadband_type, deadband_value):
        super().__init__()
        self.ui = Ui_MiOptionsDialog()
        self.ui.setupUi(self)

        self._init_fields(sampling_interval, queue_size, discard_oldest, filter, datachange_trigger, deadband_type, deadband_value)

        self.ui.dataChangeFilter.clicked.connect(self.enable_filter)
        self.ui.saveButton.clicked.connect(self.accept)

    @trycatchslot
    def _init_fields(self, sampling_interval, queue_size, discard_oldest, filter, datachange_trigger, deadband_type, deadband_value):
        self.ui.samplingInterval.setValue(sampling_interval)
        self.ui.queueSize.setValue(queue_size)
        self.ui.discardOldest.setChecked(discard_oldest)
        self.ui.dataChangeFilter.setChecked(filter)
        self.ui.dataChangeTrigger.addItems(["Status", "Status/Value", "Status/Value/Timestamp"])
        self.ui.dataChangeTrigger.setCurrentIndex(datachange_trigger)
        self.ui.deadbandType.addItems(["None", "Absolute", "Percent"])
        self.ui.deadbandType.setCurrentIndex(deadband_type)
        self.ui.deadbandValue.setValue(deadband_value)
        if not self.ui.dataChangeFilter.isChecked():
            self.enable_filter(False)

    def enable_filter(self, checked):
        self.ui.dataChangeTrigger.setEnabled(checked)
        self.ui.deadbandType.setEnabled(checked)
        self.ui.deadbandValue.setEnabled(checked)

    def get_selected_options(self):
        return self.ui.samplingInterval.value(), self.ui.queueSize.value(), self.ui.discardOldest.isChecked(), \
               self.ui.dataChangeFilter.isChecked(), self.ui.dataChangeTrigger.currentIndex(), \
               self.ui.deadbandType.currentIndex(), self.ui.deadbandValue.value()
