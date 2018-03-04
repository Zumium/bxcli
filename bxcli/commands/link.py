import click
import os.path
from terminaltables import AsciiTable

from ..tfclient import LinkServiceSession
from ..tf.boxes.LinkService import LinkType
from ..util import parse_inner_path, ask_sure, report_exception


@click.command(name='link', short_help='create link')
@click.argument('inner_src', type=str)
@click.argument('dst', type=str)
@click.option('--soft/--hard', default=True, help='Create soft or hard link, default to soft')
@report_exception
def link(inner_src, dst, soft):
    """Create link of src to destination location"""
    id, inner_path = parse_inner_path(inner_src)
    if dst[-1] == os.sep:
        dst = os.path.join(dst, os.path.basename(inner_path))

    if soft:
        ltype = LinkType.SOFT
    else:
        ltype = LinkType.HARD

    with LinkServiceSession() as client:
        client.create(id, inner_path, dst, ltype)


@click.command(name='ls-link', short_help='list links')
@click.argument('target', type=str, default='all')
@report_exception
def ls_link(target):
    """List links"""
    table_array = [['Type', 'Source', 'Location']]
    for l in query_links(target):
        if l.type == LinkType.SOFT:
            t = 'S'
        else:
            t = 'H'
        # print('{} {}:{} {}'.format(t, l.boxId, l.innerPath, l.destination))
        table_array.append([t, '{}:{}'.format(l.boxId, l.innerPath), l.destination])
    print(AsciiTable(table_array).table)


def query_links(target):
    with LinkServiceSession() as client:
        if target == 'all':
            return client.lsAll()
        splited = target.split(':')
        if len(splited) == 1:
            return client.lsBox(int(splited[0]))
        elif len(splited) == 2:
            return client.lsInner(int(splited[0]), splited[1])
        else:
            raise Exception('bad format')


@click.command(name='rm-link', short_help='remove links')
@click.option('--all', '-a', is_flag=True, help='Remove all links')
@click.option('--id', '-i', default = 0, help='Specify link id')
@click.option('--destination', '-d', default='', help='Specify link location')
@click.option('--box-path', '-b', default='', help='Specify box id')
@report_exception
def rm_link(all, id, destination, box_path):
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
        elif box_path != '':
            splited = box_path.split(':')
            if len(splited) == 1:
                box_id = int(splited[0])
                if not ask_sure('remove links of box with id {}'.format(box_id)):
                    print('Operation cancelled')
                    return
                client.removeByBox(box_id)
            elif len(splited) == 2:
                box_id, inner_path = int(splited[0]), splited[1]
                if not ask_sure('remove links of file {}:{}'.format(box_id, inner_path)):
                    print('Operation cancelled')
                    return
                client.removeByInner(box_id, inner_path)
        else:
            print('No details have been specified, please read help')
            return
