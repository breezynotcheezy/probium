class FastbackError(Exception):
    """Operation error"""
class UnsupportedType(FastbackError):
    """specified engine unavailable"""
class EngineFailure(FastbackError):
    """Engine integration exception"""
