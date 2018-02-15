import click
from terminaltables import AsciiTable

from ..tfclient import BoxServiceSession
from ..util import ask_sure, report_exception
from ..tf.boxes.BoxService import BoxStatus


@click.group()
def box():
    """Box operations"""
    pass


@click.command(name='create')
@click.argument('name', nargs=1)
@click.option('--description', '-d', type=str, default='', help='Description message of the new box')
@report_exception
def create(name,description):
    """Create new box"""
    with BoxServiceSession() as client:
        client.create(name,description)


@click.command(name='remove')
@click.argument('id', nargs=1, type=int)
@report_exception
def remove(id):
    """Remove a specific box"""
    if not ask_sure('remove box with id {}'.format(id)):
        print('Operation cancelled')
        return
    with BoxServiceSession() as client:
        client.remove(id)


@click.command(name='set-description')
@click.argument('id', nargs=1, type=int)
@click.argument('description', nargs=1, type=str)
@report_exception
def set_description(id, description):
    """Set description of a specific box"""
    with BoxServiceSession() as client:
        client.setDescription(id, description)


@click.command(name='set-name')
@click.argument('id', nargs=1, type=int)
@click.argument('name', nargs=1, type=str)
@report_exception
def set_name(id, name):
    """Set name of a specific box"""
    with BoxServiceSession() as client:
        client.setDescription(id, name)


@click.command(name='archive')
@click.argument('id', nargs=1, type=int)
@report_exception
def archive(id):
    """Archive an opened box"""
    with BoxServiceSession() as client:
        client.archive(id)


@click.command(name='unarchive')
@click.argument('id', nargs=1, type=int)
@report_exception
def unarchive(id):
    """Unarchive an archived box"""
    with BoxServiceSession() as client:
        client.unarchive(id)


@click.command(name='list')
@report_exception
def list():
    """List all boxes"""
    with BoxServiceSession() as client:
        boxes = client.currentBoxes()

        table = [
            ['ID', 'Name', 'Description', 'Status', 'CreatedAt']
        ]
        for b in boxes:
            table.append([b.id, b.name, b.description, BoxStatus._VALUES_TO_NAMES[b.status], b.createdAt])
        t = AsciiTable(table)
        print(t.table)


@click.command(name='inspect')
@click.argument('id', type=int)
@report_exception
def inspect(id):
    """Inspect the detail info of a box"""
    with BoxServiceSession() as client:
        box = client.get(id)
        table = [
            ['ID', box.id],
            ['Name', box.name],
            ['Description', box.description],
            ['Status', BoxStatus._VALUES_TO_NAMES[box.status]],
            ['CreatedAt', box.createdAt]
        ]
        t = AsciiTable(table)
        t.inner_row_border = True
        print(t.table)


box.add_command(create)
box.add_command(remove)
box.add_command(set_description)
box.add_command(set_name)
box.add_command(archive)
box.add_command(unarchive)
box.add_command(list)
box.add_command(inspect)