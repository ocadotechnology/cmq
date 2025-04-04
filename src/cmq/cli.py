import click
import json
import os
import sys

from cmq.plugin import PluginManager


def save_to_file(data, output):
    output.write(json.dumps(data, indent=2))


@click.command()
@click.argument('query', required=False)
@click.option('-v', '--verbose', is_flag=True, default=False, help='Enable verbose output')
@click.option('-o', '--output', type=click.File('w'), default=sys.stdout, help='Output file')
def main(query, verbose, output):

    if verbose:
        os.environ["CMQ_VERBOSE_OUTPUT"] = "true"

    result = eval(query, PluginManager().get_sessions())
    if result:
        output.write(result if isinstance(result, str) else json.dumps(result, indent=2, default=str))
        output.write('\n')


if __name__ == '__main__':
    main()