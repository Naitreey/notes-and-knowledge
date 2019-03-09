flag = object()

# or
class _Flag:

  __instance = None

  def __new__(cls):
    if cls.__instance is None:
      cls.__instance = object.__new__(cls)
    return cls.__instance

# or
class _Flag(Enum):
  flag = auto()

flag = _Flag.flag
