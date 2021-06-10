class PolygonError(Exception):
    def __init__(self, message):
        self.message = message


class SelfIntersection(PolygonError):
    pass


class CutterError(PolygonError):
    pass


class UnableToClose(CutterError):
    pass


class NonConvex(CutterError):
    pass


class DegenerateCutter(CutterError):
    pass


class DegenerateEdge(CutterError):
    pass
