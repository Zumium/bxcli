import click
import os.path

from ..tfclient import FileServiceSession
from ..tf.boxes.FileService import AddBy, FetchBy, LsType
from ..util import parse_inner_path, ask_sure, report_exception


@click.group()
def file():
    """File operations"""
    pass


@click.command(name='add')
@click.argument('inner_dst', type=str)
@click.argument('outer_src', type=str)
@click.option('--move/--copy', default=True)
@report_exception
def add(inner_dst, outer_src, move):
    """Add a file to the specific path inside a box"""
    id, inner_path = parse_inner_path(inner_dst)
    inner_path = os.path.join(inner_path, os.path.basename(outer_src))

    if move:
        add_by = AddBy.MOVE
    else:
        add_by = AddBy.COPY

    with FileServiceSession() as client:
        client.add(id, inner_path, outer_src, add_by)


@click.command(name='fetch')
@click.argument('inner_src', type=str)
@click.argument('outer_dst', type=str)
@click.option('--move/--copy', default=True)
@report_exception
def fetch(inner_src, outer_dst, move):
    """Fetch file from the specific box"""
    id, inner_path = parse_inner_path(inner_src)
    outer_dst = os.path.join(outer_dst, os.path.basename(inner_path))

    if move:
        fetch_by = FetchBy.MOVE
    else:
        fetch_by = FetchBy.COPY

    with FileServiceSession() as client:
        client.fetch(id, inner_path, outer_dst, fetch_by)


@click.command(name='remove')
@click.argument('inner_path', type=str)
@report_exception
def remove(inner_path):
    """Remove a file or dir inside a box"""
    if not ask_sure('remove {}'.format(inner_path)):
        print('Operation cancelled')
        return
    id, path = parse_inner_path(inner_path)
    with FileServiceSession() as client:
        client.remove(id, path)


@click.command(name='ls')
@click.argument('inner_dir')
@report_exception
def ls(inner_dir):
    """List all files inside a inner dir"""
    id, path = parse_inner_path(inner_dir)
    with FileServiceSession() as client:
        flist = client.ls(id, path)
    for f in flist:
        if f.type == LsType.DIR:
            t = 'd'
        else:
            t = 'f'
        print('{} {}'.format(t, f.name))


@click.command(name='move')
@click.argument('inner_src')
@click.argument('inner_dst')
@report_exception
def move(inner_src, inner_dst):
    """Move file or dir between two boxes"""
    src_id, src_path = parse_inner_path(inner_src)
    dst_id, dst_path = parse_inner_path(inner_dst)

    with FileServiceSession() as client:
        client.move(src_id, src_path, dst_id, dst_path)


@click.command(name='copy')
@click.argument('inner_src')
@click.argument('inner_dst')
@report_exception
def copy(inner_src, inner_dst):
    """Move file or dir between two boxes"""
    src_id, src_path = parse_inner_path(inner_src)
    dst_id, dst_path = parse_inner_path(inner_dst)

    with FileServiceSession() as client:
        client.copy(src_id, src_path, dst_id, dst_path)


@click.command(name='inner-move')
@click.argument('id', type=int)
@click.argument('src', type=str)
@click.argument('dst', type=str)
@report_exception
def inner_move(id, src, dst):
    """Move file or dir in box"""
    with FileServiceSession() as client:
        client.innerMove(id, src, dst)


@click.command(name='inner-copy')
@click.argument('id', type=int)
@click.argument('src', type=str)
@click.argument('dst', type=str)
@report_exception
def inner_copy(id, src, dst):
    """Move file or dir in box"""
    with FileServiceSession() as client:
        client.innerCopy(id, src, dst)


file.add_command(add)
file.add_command(fetch)
file.add_command(remove)
file.add_command(ls)
file.add_command(move)
file.add_command(copy)
file.add_command(inner_move)
file.add_command(inner_copy)

