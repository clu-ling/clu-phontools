from setuptools import setup
import os

from clu.phontools.info import info

# use requirements.txt as deps list
with open("requirements.txt", "r") as f:
    required = f.read().splitlines()

# get readme
with open("README.md", "r") as f:
    readme = f.read()

test_deps = required + ["green", "coverage", "mypy"]
# NOTE: <packagename> @ allows installation of git-based URLs
dev_deps = test_deps + [
    "black",
    "wheel",
    "mkdocs",
    # "portray @ git+git://github.com/myedibleenso/portray.git@issue/83",
    # "portray @ git+git://github.com/myedibleenso/portray.git@avoid-regressions",
    # "mkapi==1.0.14",
    "pdoc3",
    "mkdocs-git-snippet",
    "mkdocs-git-revision-date-localized-plugin",
    "mkdocs-git-authors-plugin",
    "mkdocs-rtd-dropdown",
    "pre-commit",
]

setup(
    name="clu-phontools",
    packages=["clu.phontools"],
    version=info.version,
    keywords=["nlp", "re-aline", "sequence alignment"],
    description=info.description,
    long_description=readme,
    url=info.repo,
    download_url=info.download_url,
    author=" and ".join(info.authors),
    author_email=info.contact,
    license=info.license,
    # see https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
    scripts=[
        os.path.join("bin", "clu-phontools-rest-api"),
        os.path.join("bin", "re-aline-excel-data"),
    ],
    install_requires=required,
    classifiers=[
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
    ],
    tests_require=test_deps,
    extras_require={
        "test": test_deps,
        # "dev": dev_deps,
        "all": dev_deps
        # 'docs': docs_deps
    },
    include_package_data=True,
    zip_safe=False,
)
