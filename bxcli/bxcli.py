#! /usr/bin/env python3
import click

from .commands.box import box
from .commands.file import file
from .commands.link import link


@click.group()
def bxcli():
    """Command line based client for Boxes"""
    pass


bxcli.add_command(box)
bxcli.add_command(file)
bxcli.add_command(link)
