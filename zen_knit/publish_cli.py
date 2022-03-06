import click
import os

from zen_knit.publish.support import cred
from zen_knit.publish.core import publish as my_publish, worker




@click.group()
def cli():
    pass


@click.command()
@click.option('--key', prompt='what is your key?', help='What is your access key?')
@click.option('--secret', prompt='what is your secret key?', help='What is your secret key?')
@click.option('--url', prompt='what is zen report url?', help='what is zen report url?')
@click.option('--profile', help='which profile do you want to use?', default='default')
def create(key, secret, url, profile):
    return cred.create(key, secret, url, profile)


@click.command()
@click.option('--key', help='What is your access key?')
@click.option('--secret', help='What is your secret key?')
@click.option('--url', help='what is zen report url?')
@click.option('--profile', help='which profile do you want to use?', default='default')
def create_w(key, secret, url, profile):
    return cred.create(key, secret, url, profile)


@click.command()
@click.option('--key', prompt='what is your access key?', help='What is your access key?')
@click.option('--secret', prompt='what is your secret key?', help='What is your secret key?')
@click.option('--profile', help='which profile do you want to use?', default='default')
def update(key, secret, profile):
    return cred.update(key, secret, profile)


@click.command()
@click.option('--key', help='What is your access key?')
@click.option('--secret', help='What is your secret key?')
@click.option('--profile', help='which profile do you want to use?', default='default')
def update_w(key, secret, profile):
    return cred.update(key, secret, profile)

@click.command()
@click.option('--path', prompt='path of report or dashboard?', default=os.getcwd(), help="folder to look into")
@click.option('--fresh', '-f', prompt='do you want to publish as fresh report',  is_flag=True,  help="run as fresh report")
@click.option('--browser','-b',prompt='do you want to open report in browser', is_flag=True, help="Want to open window")
@click.option('--profile', prompt='which profile do you want to use?', help='which profile do you want to use?', default='default')
def publish(path, fresh, browser, profile):
    return my_publish.publish(path, fresh, browser, profile)


@click.command()
@click.option('--path', default=os.getcwd(), help="folder to look into")
@click.option('--fresh', '-f', is_flag=True,  help="run as fresh report")
@click.option('--browser','-b', is_flag=True, help="Want to open window")
@click.option('--profile', help='which profile do you want to use?', default='default')
def publish_w(path, fresh, browser, profile):
    return my_publish.publish_w(path, fresh, browser, profile)

@click.command()
@click.option('--profile', help='which profile do you want to use?', default='default')
def get_workers(profile):
    return worker.get_workers(profile)

@click.command()
@click.option('--profile', help='which profile do you want to use?', default='default')
def get_worker_group(profile):
    return worker.get_worker_groups(profile)



cli.add_command(update)
cli.add_command(update_w)

cli.add_command(create)
cli.add_command(create_w)

cli.add_command(publish)
cli.add_command(publish_w)

cli.add_command(get_workers)
cli.add_command(get_worker_group)
