import click

from helpers import format_dicts_as_table


@click.command()
@click.option("--name", prompt=True, required=True, type=str)
@click.option("--description", prompt=True, required=True, type=str, default="")
@click.pass_context
def add_task(ctx, name, description):
    db = ctx.obj.get("db")
    db.add_task(name, description)
    click.echo(f"Task '{name}' has been added")

@click.command()
@click.option("--name", prompt=True, required=True, type=str)
@click.pass_context
def complete_task(ctx, name):
    db = ctx.obj.get("db")
    db.complete_task(name, "Yes")
    click.echo(f"Task '{name}' has been updated")

@click.command()
@click.option("--name", prompt=True, required=True, type=str)
@click.pass_context
def get_task(ctx, name):
    db = ctx.obj.get("db")
    task = db.get_task(name)
    click.echo(format_dicts_as_table([task]))

@click.command()
@click.pass_context
def list_tasks(ctx):
    db = ctx.obj.get("db")
    tasks = db.list_tasks()
    click.echo(format_dicts_as_table(tasks))


@click.command()
@click.option("--name", prompt=True, required=True, type=str)
@click.pass_context
def delete_task(ctx, name):
    db = ctx.obj.get("db")
    db.remove_task(name)
    click.echo(f"Task '{name}' has been removed")