from PyQt5.QtWidgets import QDialog

from dialogs.sub_options_ui import Ui_SubOptionsDialog
from utils import trycatchslot


class SubOptionsDialog(QDialog):
    def __init__(self, requested_publishing_interval, requested_max_keep_alive_count, requested_lifetime_count, max_notifications_per_publish):
        super().__init__()
        self.ui = Ui_SubOptionsDialog()
        self.ui.setupUi(self)

        self._init_fields(requested_publishing_interval, requested_max_keep_alive_count, requested_lifetime_count, max_notifications_per_publish)

        self.ui.saveButton.clicked.connect(self.accept)

    @trycatchslot
    def _init_fields(self, requested_publishing_interval, requested_max_keep_alive_count, requested_lifetime_count, max_notifications_per_publish):
        self.ui.requestedPublishInterval.setValue(requested_publishing_interval)
        self.ui.requestedMaxKeepAliveCount.setValue(requested_max_keep_alive_count)
        self.ui.requestedLifeTimeCount.setValue(requested_lifetime_count)
        self.ui.maxNotificationsPerPublish.setValue(max_notifications_per_publish)

    def get_selected_options(self):
        return self.ui.requestedPublishInterval.value(), self.ui.requestedMaxKeepAliveCount.value(), \
               self.ui.requestedLifeTimeCount.value(), self.ui.maxNotificationsPerPublish.value()
