#! /usr/bin/env python3
import click

from .commands import box
from .commands import file
from .commands import link

VERSION = '1.0'

@click.group()
@click.version_option(VERSION)
def bxcli():
    """Command line based client for Boxes"""
    pass


bxcli.add_command(box.create)
bxcli.add_command(box.remove)
bxcli.add_command(box.set_name)
bxcli.add_command(box.set_description)
bxcli.add_command(box.archive)
bxcli.add_command(box.unarchive)
bxcli.add_command(box.list)
bxcli.add_command(box.inspect)

bxcli.add_command(file.add)
bxcli.add_command(file.fetch)
bxcli.add_command(file.rm)
bxcli.add_command(file.ls)
bxcli.add_command(file.copy)
bxcli.add_command(file.move)

bxcli.add_command(link.link)
bxcli.add_command(link.ls_link)
bxcli.add_command(link.rm_link)
