from setuptools import setup, find_packages

requires = [
    'requests',
    'pyyaml',
    'influxdb',
]

setup(
    name='solaredge_to_influxdb',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
)
