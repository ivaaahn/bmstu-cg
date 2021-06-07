class CutterError(Exception):
    def __init__(self, message):
        self.message = message


class UnableToClose(CutterError):
    pass


class NonConvex(CutterError):
    pass
