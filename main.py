import click

import password_commands
import task_commands
from db_interactions import DB


@click.group(chain=True, invoke_without_command=True)
@click.pass_context
def cli(ctx):
    try:
        pass
    except:
        click.echo("Entered option is invalid")

cli.add_command(password_commands.add_pass)
cli.add_command(password_commands.list_pass)
cli.add_command(password_commands.get_pass)
cli.add_command(password_commands.change_pass)
cli.add_command(password_commands.delete_pass)

cli.add_command(task_commands.add_task)
cli.add_command(task_commands.list_tasks)
cli.add_command(task_commands.get_task)
cli.add_command(task_commands.complete_task)
cli.add_command(task_commands.delete_task)



if __name__ == '__main__':
    cli(obj={"db": DB()})