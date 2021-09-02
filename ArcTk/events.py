from gui.windows import BoxEntryWindow


class EventManager():
    def __init__(self, app):
        self.app = app

    def initialize(self, target: str):
        # This prevents window from opening on launch
        if target == "box_entry_window":
            self.app.widgets[target] = BoxEntryWindow(self.app)

    def get(self, target: str):
        return self.app.widgets[target].get()

    def set(self, target: str, **kwargs):
        self.app.widgets[target].set(**kwargs)

    def refresh(self, target: str):
        self.app.widgets[target].refresh()

    def update(self, target: str):
        self.app.widgets[target].update()
