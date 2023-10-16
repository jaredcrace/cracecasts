import os
import dotenv
import argparse
from icecream import ic
from rich import print
from rich.table import Table
from rich.console import Console
from rich.markdown import Markdown
from loguru import logger

dotenv.load_dotenv()


if __name__ == '__main__':

    ## 1. argparse
    description_text = '''
    Here is a really great description of my new script. It is awesome.  

    The algorithm for this script does the following: 
        - it starts up 
        - it prints to the screen 
        - it closes 

    Note - Here are some final notes about the script
    '''

    example_text = '''
    Examples:
    $ python3 main_arg.py input_file  

    $ python3 main_arg.py input_file  -v 
    '''

    parser = argparse.ArgumentParser(description=description_text,
                                     epilog=example_text,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

   
    parser.add_argument('input_file',
                        help='input file',
                        action='store',
                        default=None)

    parser.add_argument('-s',
                        '--sample',
                        help=
                        '''Here is a long help section about this --sample parameter. Argparse 
                        handles this very well and ensures that it is formated correctly. 
                        ''',
                        action='store',
                        default=None)

    parser.add_argument('-v',
                        '--verbose',
                        help='verbose debug printing',
                        action='store_true',
                        default=False)

    args = parser.parse_args()

    print(f"{args.verbose}")
    print(f"{args.input_file}")

    ## 2. dotenv
    secret = os.environ.get('secret_key')
    print(f"secret_key is: {secret}")

    ## 3. ice
    ic(secret)

    foo_array = []
    foo_array.append("jared")
    foo_array.append("rusty")
    foo_array.append("jun")
    ic(foo_array)

    foo_dict = {
        'model': "gpt-4",
        'key': 'api_key'
    }
    ic(foo_dict)


    ## 4. rich
    print("[red]This is red text")
    print("[blue]This is blue text")

    console = Console()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=10)
    table.add_column("Name")
    table.add_column("Description")

    table.add_row("1", "Foo", "The first item")
    table.add_row("2", "Bar", "The second item")
    table.add_row("3", "Baz", "The third item")

    console.print(table)

    markdown = Markdown("# This is a header\n\n- This\n- is\n- a\n- list\n")

    console.print(markdown)


    ## 5. loguru
    logger.add("my_log.log", rotation="1 day")  # New file is created each day
    logger.info("added file")
    logger.error("error to file")
