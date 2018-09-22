import pytest

from plotlyink.testing import compare_dict


@pytest.mark.parametrize(
    'inputs',
    [
        # Corner Case:
        {
            'dict1': {},
            'dict2': {},
            'expected': (True, ""),
        },

        # Not same keys:
        {
            'dict1': {
                'key1': None,
                'key2': None,
                'key3': None
            },
            'dict2': {
                'key1': None,
                'key3': None
            },
            'expected': (
                False, "['key1', 'key2', 'key3'] should be ['key1', 'key3']"),
        },

        # Same keys but not same order:
        {
            'dict1': {
                'key1': None,
                'key2': None,
                'key3': None
            },
            'dict2': {
                'key1': None,
                'key3': None,
                'key2': None
            },
            'expected': (True, ""),
        },

        # Lists:
        {
            'dict1': {
                'list_of_nums': [1.98904, 2, 3],
                'list_of_str': ['scatter', 'ok', 'kitkats']
            },
            'dict2': {
                'list_of_nums': [1.98904, 2, 3],
                'list_of_str': ['scatter', 'ok', 'kitkats']
            },
            'expected': (True, ''),
        },
        {
            'dict1': {
                'list_of_nums': [1.98904, 2, 3],
                'list_of_str': ['scatter', 'ok', 'kitkat']
            },
            'dict2': {
                'list_of_nums': [1.98904, 2, 3],
                'list_of_str': ['scatter', 'ok', 'kitkats']
            },
            'expected': (
                False,
                "'list_of_str' -> ['scatter', 'ok', 'kitkat'] should be ['scatter', 'ok', 'kitkats']"
            ),
        },
        {
            'dict1': {
                'list_of_nums': [1.9890454845564, 2, 3],
                'list_of_str': ['scatter', 'ok', 'kitkats']
            },
            'dict2': {
                'list_of_nums': [1.98904, 2, 3],
                'list_of_str': ['scatter', 'ok', 'kitkats']
            },
            'expected': (
                False,
                "'list_of_nums' -> [1.9890454845564, 2, 3] should be [1.98904, 2, 3]"
            ),
        },

        # Embed dicts:
        {
            'dict1': {
                'dict_of_nums': {
                    'num1': 1,
                    'num2': 3
                },
                'dict_of_bool': {
                    'bool1': True,
                    'bool2': False
                },
            },
            'dict2': {
                'dict_of_nums': {
                    'num1': 1,
                    'num2': 3
                },
                'dict_of_bool': {
                    'bool1': True,
                    'bool2': False
                },
            },
            'expected': (True, ""),
        },
        {
            'dict1': {
                'dict_of_nums': {
                    'num1': 1,
                    'num2': 3
                },
                'dict_of_bool': {
                    'bool1': True,
                    'bool2': False
                },
            },
            'dict2': {
                'dict_of_nums': {
                    'num1': 1,
                    'num2': 2
                },
                'dict_of_bool': {
                    'bool1': True,
                    'bool2': False
                },
            },
            'expected': (False, "'num2' -> 3 should be 2"),
        },

        # Mixing types
        {
            'dict1': {
                'data': [{'x': ['chocolat', 'apple'],
                          'y': [1, 3]}],
                'layout': {'yaxis': 'pretty'},
            },
            'dict2': {
                'data': [{'x': ['chocolat', 'apple'],
                          'y': [1, 2]}],
                'layout': {'yaxis': 'pretty'},
            },
            'expected': (
                False,
                "'y' -> [1, 3] should be [1, 2]"
            ),
        },
    ])
def test_compare_dict(inputs):
    dict1, dict2, expected = inputs.values()
    equivalent, msg = compare_dict(dict1, dict2)
    assert msg == expected[1]
    assert equivalent == expected[0]
