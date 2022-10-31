from setuptools import setup, find_packages

setup(
    name='chalan',
    version='0.1.0',
    description='Elasticsearch migrations tool',
    url='https://github.com/anandtripathi5/chalan',
    author='Anand Tripathi',
    author_email='anand.tripathi507@gmail.com',
    license='MIT License',
    packages=find_packages(),  # list of all packages,
    include_package_data=True,
    keyword="chalan, chalan elasticsearch tool, elasticsearch migration tool",
    install_requires=['elasticsearch>8.0.0', 'typer==0.6.1', 'rich==12.5.1'],
    entry_points='''
        [console_scripts]
        chalan=src.commands:app
    ''',
    package_data={'': ['templates/*.mako']},
)
