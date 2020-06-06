from datetime import datetime

from PyQt5.QtCore import pyqtSignal, QObject


class DataChangeHandler(QObject):
    data_change_fired = pyqtSignal(object, str, int, str)

    def datachange_notification(self, node, val, data):
        status_code = data.monitored_item.Value.StatusCode.value
        if data.monitored_item.Value.SourceTimestamp:
            timestamp = data.monitored_item.Value.SourceTimestamp.isoformat()
        elif data.monitored_item.Value.ServerTimestamp:
            timestamp = data.monitored_item.Value.ServerTimestamp.isoformat()
        else:
            timestamp = datetime.now().isoformat()
        self.data_change_fired.emit(node, str(val), status_code, timestamp)
