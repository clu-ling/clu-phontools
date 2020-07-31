# get version
with open('realine/__init__.py', 'r', 'utf-8') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)



class ReAlineDevelop(develop):
    def run(self):
        develop.run(self)


class ReAlineInstall(install):
    def run(self):
        # install everything else
        install.run(self)


# use requirements.txt as deps list
with open('requirements.txt', 'r', 'utf-8') as f:
    required = f.read().splitlines()

# get readme
with open('../README.md', 'r', 'utf-8') as f:
    readme = f.read()

test_deps = ["green>=2.5.0", "coverage"]

setup(name='re-aline',
      packages=["realine"],
      version=version,
      keywords=['nlp', 'alignment', 'speech'],
      description="A successor to the phonetic alignment algorithm ALINE.",
      long_description=readme,
      url='https://github.com/clu-ling/re-aline',
      download_url="https://github.com/clu-ling/re-aline/archive/v{}.zip".format(version),
      author='myedibleenso',
      author_email='gus@parsertongue.org',
      license='Apache 2.0',
      install_requires=required,
      cmdclass={
        'install': ReAlineInstall,
        'develop': ReAlineDevelop,
      },
      classifiers=(
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3"
      ),
      tests_require=test_deps,
      extras_require={
        'test': test_deps,
        'jupyter': viz_deps
      },
      include_package_data=True,
      zip_safe=False)
