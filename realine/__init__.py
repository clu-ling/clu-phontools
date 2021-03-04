try:
  from .realine import ReAline
  from .pronouncing import PronouncingDict
except Exception as e:
  print("Failed to import ReAline")
  print(e)

try:
  from .info import info
  __version__ = info.version
except:
  print("Failed to improt info")
