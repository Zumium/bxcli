import click
import os.path
from terminaltables import AsciiTable

from ..tfclient import FileServiceSession
from ..tf.boxes.FileService import AddBy, FetchBy, LsType
from ..util import parse_inner_path, ask_sure, report_exception


@click.command(name='add', short_help='add to box')
@click.argument('inner_dst', type=str)
@click.argument('outer_src', type=str)
@click.option('--move/--copy', default=True, help='Add by move or copy, default to move')
@report_exception
def add(inner_dst, outer_src, move):
    """Add a file or dir to the specific path inside a box"""
    id, inner_path = parse_inner_path(inner_dst)
    inner_path = os.path.join(inner_path, os.path.basename(outer_src))

    if move:
        add_by = AddBy.MOVE
    else:
        add_by = AddBy.COPY

    with FileServiceSession() as client:
        client.add(id, inner_path, outer_src, add_by)


@click.command(name='fetch', short_help='fetch from box')
@click.argument('inner_src', type=str)
@click.argument('outer_dst', type=str)
@click.option('--move/--copy', default=True, help='Fetch by move or copy, default to move')
@report_exception
def fetch(inner_src, outer_dst, move):
    """Fetch file or dir from the specific box"""
    id, inner_path = parse_inner_path(inner_src)
    outer_dst = os.path.join(outer_dst, os.path.basename(inner_path))

    if move:
        fetch_by = FetchBy.MOVE
    else:
        fetch_by = FetchBy.COPY

    with FileServiceSession() as client:
        client.fetch(id, inner_path, outer_dst, fetch_by)


@click.command(name='rm', short_help='remove from box')
@click.argument('inner_path', type=str)
@report_exception
def rm(inner_path):
    """Remove a file or dir inside a box"""
    if not ask_sure('remove {}'.format(inner_path)):
        print('Operation cancelled')
        return
    id, path = parse_inner_path(inner_path)
    with FileServiceSession() as client:
        client.remove(id, path)


@click.command(name='ls', short_help='list files inside a box')
@click.argument('inner_dir')
@report_exception
def ls(inner_dir):
    """List all files and dirs inside a inner dir"""
    id, path = parse_inner_path(inner_dir)
    with FileServiceSession() as client:
        flist = client.ls(id, path)
    table_array = [['Type','Name']]
    for f in flist:
        if f.type == LsType.DIR:
            t = 'D'
        else:
            t = 'F'
        table_array.append([t, f.name])
    print(AsciiTable(table_array).table)


@click.command(name='move', short_help='move files among boxes')
@click.argument('inner_src')
@click.argument('inner_dst')
@report_exception
def move(inner_src, inner_dst):
    """Move file or dir between two boxes"""
    src_id, src_path = parse_inner_path(inner_src)
    dst_id, dst_path = parse_inner_path(inner_dst)

    dst_path = os.path.join(dst_path, os.path.basename(src_path))

    with FileServiceSession() as client:
        if src_id != dst_id:
            client.move(src_id, src_path, dst_id, dst_path)
        else:
            client.innerMove(src_id, src_path, dst_path)


@click.command(name='copy', short_help='copy files among boxes')
@click.argument('inner_src')
@click.argument('inner_dst')
@report_exception
def copy(inner_src, inner_dst):
    """Move file or dir between two boxes"""
    src_id, src_path = parse_inner_path(inner_src)
    dst_id, dst_path = parse_inner_path(inner_dst)

    dst_path = os.path.join(dst_path, os.path.basename(src_path))

    with FileServiceSession() as client:
        if src_id == dst_id:
            client.copy(src_id, src_path, dst_id, dst_path)
        else:
            client.innerCopy(src_id, src_path, dst_path)
