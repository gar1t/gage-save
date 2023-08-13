from vml._internal import click_util
from vml._vendor import click

from .check import check


@click.group(cls=click_util.Group)
def main():
    pass

main.add_command(check)
