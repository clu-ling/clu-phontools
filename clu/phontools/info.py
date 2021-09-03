from typing import List


class AppInfo:
    """
    General information about the application.
    """

    version: str = "0.1-beta"
    description: str = "Re-Aline."
    authors: List[str] = ["myedibleenso", "elsayed-issa", "mohmdsh"]
    contact: str = "gus@parsertongue.org"
    repo: str = "https://github.com/clu-ling/clu-phontools"
    license: str = "Apache 2.0"

    @property
    def download_url(self) -> str:
        return f"{self.repo}/archive/v{self.version}.zip"


info = AppInfo()
