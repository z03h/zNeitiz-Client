import re
from setuptools import setup



version = '0.0.0'
with open('zneitiz/__init__.py') as f:
    version = re.search(r'^__version__.+=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE)
    if version:
        version = version.group(1)

if not version:
    raise RuntimeError('version is not set')


readme = ''
with open('README.md') as f:
    readme = f.read()

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

packages = [
    'zneitiz'
]

setup(name='zneitiz',
      author='z03h',
      url='https://github.com/z03h/zNeitiz-Client',
      version=version,
      packages=packages,
      license='MPL-2.0',
      description='Python wrapper for zNeitiz API',
      long_description=readme,
      long_description_content_type="text/markdown",
      include_package_data=True,
      #install_requires=requirements,
      python_requires='>=3.9.0',
)
