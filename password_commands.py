import click
import subprocess


from helpers import format_dicts_as_table
from passwords_helper import check_pass_complexity, encrypt_password, decrypt_password, generate_strong_password

KEY = b'LGvyonxVcBtQ_hex3mYy28C1eWbwZ1aYM9_txSW0Lp0='

@click.command()
@click.option("--name", prompt=True, required=True, type=str)
@click.option("--username", prompt=True, required=False, type=str, default="")
@click.password_option("--password", prompt=True, confirmation_prompt=True, callback=check_pass_complexity, hide_input=True, required=True, type=str)
@click.pass_context
def add_pass(ctx, name, username, password):
    db = ctx.obj.get("db")
    if name and password:
        encrypted_password = encrypt_password(KEY, password)
        db.add_password(name, username, encrypted_password)
        click.echo("Password added successfully!")
    else:
        click.echo("Please fill in all required fields.")


@click.command()
@click.pass_context
def list_pass(ctx):
    db = ctx.obj.get("db")
    passwords = db.list_passwords()
    ctx.obj["list"] = format_dicts_as_table(passwords)
    return

@click.command()
@click.option("--name", "-n", prompt="Enter password name", hide_input=True, required=True)
@click.pass_context
def get_pass(ctx, name):
    db = ctx.obj.get("db")
    pass_data = db.get_password(name)
    pass_data["password"] = decrypt_password(KEY, pass_data["password"])
    format_dicts_as_table([pass_data])
    return


@click.command()
@click.option("--name", prompt=True, required=True, type=str)
@click.pass_context
def delete_pass(ctx, name):
    db = ctx.obj.get("db")
    db.delete_password(name)
    click.echo(f"Password {name} has been deleted")
    return name


@click.command()
@click.option("--name", prompt="Enter password name for change", required=True, type=str)
@click.option("--username", prompt=True, required=False, type=str, default="")
@click.password_option("--password", prompt=True, confirmation_prompt=True, callback=check_pass_complexity, hide_input=True, required=True, type=str)
@click.pass_context
def change_pass(ctx, name, username, password):
    db = ctx.obj.get("db")
    db.update_password(name, username, password)
    click.echo(f"Password with name {name} has been updated.")
    return name

@click.command()
@click.option("--l", "-length", prompt="Enter password length", show_default=True, default=12, required=True, type=int, help="Password lenght")
@click.option("--d", "-digits", is_flag=True, show_default=True, default=True, help="Include digits in password")
@click.option("--s", "-symbols", is_flag=True, show_default=True, default=True, help="Include special symbols in password")
def gen_pass(l, d, s):
    password = generate_strong_password(l, d, s)
    subprocess.run("pbcopy", text=True, input=password)
    click.echo(f"Password generated and has been copied to clipboard")
