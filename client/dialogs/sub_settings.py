from PyQt5.QtWidgets import QDialog

from dialogs.sub_settings_ui import Ui_SubSettingsDialog
from utils import trycatchslot


class SubSettingsDialog(QDialog):
    def __init__(self, requested_publishing_interval, requested_max_keep_alive_count, requested_lifetime_count, max_notifications_per_publish, priority):
        super().__init__()
        self.ui = Ui_SubSettingsDialog()
        self.ui.setupUi(self)

        self._init_fields(requested_publishing_interval, requested_max_keep_alive_count, requested_lifetime_count, max_notifications_per_publish, priority)

        self.ui.requestedMaxKeepAliveCount.valueChanged.connect(self.adjust_life_time)
        self.ui.requestedLifeTimeCount.valueChanged.connect(self.adjust_keep_alive)
        self.ui.cancelButton.clicked.connect(self.reject)
        self.ui.createButton.clicked.connect(self.accept)

    @trycatchslot
    def _init_fields(self, requested_publishing_interval, requested_max_keep_alive_count, requested_lifetime_count, max_notifications_per_publish, priority):
        self.ui.requestedPublishInterval.setValue(requested_publishing_interval)
        self.ui.requestedMaxKeepAliveCount.setValue(requested_max_keep_alive_count)
        self.ui.requestedLifeTimeCount.setValue(requested_lifetime_count)
        self.ui.maxNotificationsPerPublish.setValue(max_notifications_per_publish)
        self.ui.priority.setValue(priority)

    def adjust_life_time(self, i):
        if self.ui.requestedLifeTimeCount.value() < 3*i:
            self.ui.requestedLifeTimeCount.setValue(3*i)

    def adjust_keep_alive(self, i):
        if self.ui.requestedMaxKeepAliveCount.value() > i//3:
            self.ui.requestedMaxKeepAliveCount.setValue(i//3)

    def get_selected_options(self):
        return self.ui.requestedPublishInterval.value(), self.ui.requestedMaxKeepAliveCount.value(), \
               self.ui.requestedLifeTimeCount.value(), self.ui.maxNotificationsPerPublish.value(), \
               self.ui.priority.value()
