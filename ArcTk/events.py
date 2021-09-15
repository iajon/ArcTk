from gui.windows import AdditionalToolsWindow, BoxEntryWindow, ExportBoxWindow, PdfNotificationWindow, SetActiveBoxWindow


class EventManager():
    def __init__(self, app):
        self.app = app

    def initialize(self, target: str):
        # This prevents window from opening on launch
        if target == "box_entry_window":
            self.app.widgets[target] = BoxEntryWindow(self.app)
        if target == "set_active_box_window":
            self.app.widgets[target] = SetActiveBoxWindow(self.app)
        if target == "export_box_window":
            self.app.widgets[target] = ExportBoxWindow(self.app)
        if target == "additional_tools_window":
            self.app.widgets[target] = AdditionalToolsWindow(self.app)
        if target == "pdf_notification_window":
            self.app.widgets[target] = PdfNotificationWindow(self.app)

    def get(self, target: str):
        return self.app.widgets[target].get()

    def set(self, target: str, **kwargs):
        self.app.widgets[target].set(**kwargs)

    def refresh(self, target: str):
        self.app.widgets[target].refresh()

    def update(self, target: str, **kwargs):
        self.app.widgets[target].update(**kwargs)

    def wipe(self, target: str,):
        self.app.widgets[target].wipe()

    # Special case for artifact entry
    def set_back(self, target: str, **kwargs):
        print('Here')
        self.app.widgets[target].set_back(**kwargs)