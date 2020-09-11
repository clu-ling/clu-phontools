from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools import setup

from realine.info import info

class PackageDevelop(develop):
    def run(self):
        develop.run(self)


class PackageInstall(install):
    def run(self):
        # install everything else
        install.run(self)


# use requirements.txt as deps list
with open('requirements.txt', 'r') as f:
    required = f.read().splitlines()

# get readme
with open('README.md', 'r') as f:
    readme = f.read()

test_deps = ["green>=2.5.0", "coverage", "mypy"]

setup(name='re-aline',
      packages=["realine"],
      version=info.version,
      keywords=['nlp', 're-aline', 'sequence alignment'],
      description=info.description,
      long_description=readme,
      url=info.repo,
      download_url=info.download_url,
      author=" and ".join(info.authors),
      author_email=info.contact,
      license=info.license,
      # see https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
      scripts=['bin/re-aline-excel-data'],
      install_requires=required,
      cmdclass={
        'install': PackageInstall,
        'develop': PackageDevelop,
      },
      classifiers=[
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3"
      ],
      tests_require=test_deps,
      extras_require={
        'test': test_deps,
        'all': test_deps + required
        # 'docs': docs_deps
      },
      include_package_data=True,
      zip_safe=False)
