import click

from merge_indicator import merge_indicator


@click.group()
def cli():
    pass


@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_file', type=click.File('wb'))
def merge_indicator(input_path, output_file):
    result = merge_indicator(input_file)
    output_file.write(result)