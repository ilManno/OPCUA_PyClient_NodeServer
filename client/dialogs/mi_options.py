from PyQt5.QtWidgets import QDialog

from dialogs.mi_settings_ui import Ui_MiSettingsDialog
from utils import trycatchslot


class MiSettingsDialog(QDialog):
    def __init__(self, sampling_interval, queue_size, discard_oldest, data_change_filter, datachange_trigger, deadband_type, deadband_value):
        super().__init__()
        self.ui = Ui_MiSettingsDialog()
        self.ui.setupUi(self)

        self._init_fields(sampling_interval, queue_size, discard_oldest, data_change_filter, datachange_trigger, deadband_type, deadband_value)

        self.ui.deadbandType.currentTextChanged.connect(self.change_maximum_deadband_value)
        self.ui.cancelButton.clicked.connect(self.reject)
        self.ui.addButton.clicked.connect(self.accept)

    @trycatchslot
    def _init_fields(self, sampling_interval, queue_size, discard_oldest, data_change_filter, datachange_trigger, deadband_type, deadband_value):
        self.ui.samplingInterval.setValue(sampling_interval)
        self.ui.queueSize.setValue(queue_size)
        self.ui.discardOldest.setChecked(discard_oldest)
        self.ui.dataChangeFilter.setChecked(data_change_filter)
        self.ui.dataChangeTrigger.addItems(["Status", "Status/Value", "Status/Value/Timestamp"])
        self.ui.dataChangeTrigger.setCurrentIndex(datachange_trigger)
        self.ui.deadbandType.addItems(["None", "Absolute", "Percent"])
        self.ui.deadbandType.setCurrentIndex(deadband_type)
        if deadband_type == 2:  # Percent
            self.ui.deadbandValue.setMaximum(100.0)
        self.ui.deadbandValue.setValue(deadband_value)

    def change_maximum_deadband_value(self, text):
        if text == "Percent":
            self.ui.deadbandValue.setMaximum(100.0)
        else:
            self.ui.deadbandValue.setMaximum(999999999999999.0)

    def get_selected_options(self):
        return self.ui.samplingInterval.value(), self.ui.queueSize.value(), self.ui.discardOldest.isChecked(), \
               self.ui.dataChangeFilter.isChecked(), self.ui.dataChangeTrigger.currentIndex(), \
               self.ui.deadbandType.currentIndex(), self.ui.deadbandValue.value()
