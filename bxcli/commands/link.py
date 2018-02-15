import click
import os.path

from ..tfclient import LinkServiceSession
from ..tf.boxes.LinkService import LinkType
from ..util import parse_inner_path, ask_sure, report_exception


@click.group()
def link():
    """Link operations"""
    pass


@click.command(name='create')
@click.argument('inner_src', type=str)
@click.argument('dst', type=str)
@click.option('--soft/--hard', default=True)
@report_exception
def create(inner_src, dst, soft):
    """Create link of src to destination location"""
    id, inner_path = parse_inner_path(inner_src)
    dst = os.path.join(dst, os.path.basename(inner_path))

    if soft:
        ltype = LinkType.SOFT
    else:
        ltype = LinkType.HARD

    with LinkServiceSession() as client:
        client.create(id, inner_path, dst, ltype)


@click.command(name='list')
@click.option('--box', '-b', default=0)
@click.option('--inner-path', '-p', default='')
@report_exception
def list(box, inner_path):
    """List links"""
    with LinkServiceSession() as client:
        if box == 0:
            links = client.lsAll()
        elif inner_path == '':
            links = client.lsBox(box)
        else:
            links = client.lsInner(box, inner_path)
    for l in links:
        if l.type == LinkType.SOFT:
            t = 'S'
        else:
            t = 'H'
        print('{} {}:{} {}'.format(t, l.boxId, l.innerPath, l.destination))


@click.command(name='remove')
@click.option('--all', '-a', is_flag=True)
@click.option('--id', '-i', default = 0)
@click.option('--destination', '-d', default='')
@click.option('--box', '-b', default=0)
@click.option('--inner-path', '-p', default='')
@report_exception
def remove(all, id, destination, box, inner_path):
    """Remove links"""
    with LinkServiceSession() as client:
        if all:
            if not ask_sure('remove all links'):
                print('Operation cancelled')
                return
            client.removeAll()
        elif destination != '':
            if not ask_sure('remove link at {}'.format(destination)):
                print('Operation cancelled')
                return
            client.removeByDestination(destination)
        elif id != 0:
            if not ask_sure('remove link of id {}'.format(id)):
                print('Operation cancelled')
                return
            client.removeById(id)
        elif box !=0 and inner_path != '':
            if not ask_sure('remove links of {}:{}'.format(box, inner_path)):
                print('Operation cancelled')
                return
            client.removeByInner(box, inner_path)
        elif box != 0:
            if not ask_sure('remove links of box with id {}'.format(box)):
                print('Operation cancelled')
                return
            client.removeByBox(box)
        else:
            print('No details have been specified, please read help')
            return


link.add_command(create)
link.add_command(list)
link.add_command(remove)
