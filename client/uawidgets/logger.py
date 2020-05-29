import logging


class QtHandler(logging.Handler):

    def __init__(self, widget):
        super().__init__()
        self.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        self.setFormatter(logging.Formatter("%(name)s - %(levelname)s - %(message)s')"))
        self.widget = widget

    def emit(self, record):
        msg = self.format(record)
        print(msg)  # print to stdout also!
        self.widget.append(msg)
