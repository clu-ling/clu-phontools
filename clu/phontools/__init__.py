# try:
#     from .alignment.realine import ReAline
# #   from .pronouncing import PronouncingDict
# #   from .scoring import Metrics
# except Exception as e:
#     print("Failed to import ReAline")
#     print(e)

try:
    from .info import info

    __version__ = info.version
except:
    print("Failed to import info")
