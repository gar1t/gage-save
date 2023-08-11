import typing as t

from vml._internal import click_util
from vml._vendor import click


@click.group(cls=click_util.Group)
def main(args: t.Any):
    print(args)
