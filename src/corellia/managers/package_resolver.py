import json
import urllib.request

class PackageResolver :
    PYPI_URL = "https://pypi.org/pypi/{}/json"

    def latest (self, package: str) -> str :
        url = self.PYPI_URL.format(package)

        with urllib.request.urlopen(url) as r :
            data = json.loads(r.read().decode())

        return data['info']['version']
    
    def resolve (self, packages: list[str]) -> dict[str, str] :
        resolved = {}

        for pkg in packages :
            resolved[pkg] = self.latest(pkg)

        return resolved
    
    