import json

import click


@click.group()
def main():
    pass


@click.command()
def gen_example_configs():
    '''
    Easily generate example configs.json file
    '''
    with open("configs.json") as f:
        configs = json.loads(f.read())
    keys = [k for k, _ in configs.items()]
    example_configs = {}
    for k in keys:
        example_configs[k] = "some_value"
    with open("configs.json.example", "w+") as f_out:
        json.dump(example_configs, f_out, indent=4, sort_keys=True)


if __name__ == "__main__":
    main.add_command(gen_example_configs)
    main()
