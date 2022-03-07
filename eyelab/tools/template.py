class Tool(object):
    def __init__(self):
        self.cursor = None
        self.button = None
        self.hot_key = None
        self.settings_widget = None

    def enable(self, view):
        pass

    def disable(self, view):
        pass

    def mouse_move_handler(self):
        pass

    def mouse_click_handler(self):
        pass
