from typing import List

class AppInfo:
    """
    General information about the application.
    """
    version: str = "0.1"
    description: str = "Re-Aline."
    authors: List[str] = ["elsayed-issa", "myedibleenso"]
    contact: str = "gus@parsertongue.org"
    repo: str = "https://github.com/clu-ling/re-aline"
    license: str = "Apache 2.0"
    
    @property
    def download_url(self) -> str: 
      return f"{self.repo}/archive/v{self.version}.zip"
    

info = AppInfo()