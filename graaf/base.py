import yaml


class Generator(object):
    pass


def get_yaml(src):
    '''
    Try to read a YAML document from the provided file.

    If it doesn't exist, return an empty dict instead.
    '''
    try:
        with open(src) as fin:
            return yaml.load(fin)
    except IOError:
        return {}
