class OutputCallbackManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OutputCallbackManager, cls).__new__(cls)
            cls._instance.callback = None
        return cls._instance

    def set_callback(self, callback):
        self.callback = callback

    def get_callback(self):
        if self.callback is None:
            return print
        return self.callback
