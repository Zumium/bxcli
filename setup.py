from setuptools import setup

setup(
    name='bxcli',
    version='1.0',
    author='Zumium',
    author_email='martin007323@gmail.com',
    description='A CLI box client',
    license='BSD-3-Clause',
    packages=[
        'bxcli',
        'bxcli.commands',
        'bxcli.tf.boxes',
        'bxcli.tf'
    ],
    entry_points="""
    [console_scripts]
    boxes = bxcli.bxcli:bxcli
    """,
    install_requires=[
        'click',
        'terminaltables',
        'thrift'
    ],
)