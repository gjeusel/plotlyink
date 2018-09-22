import numpy as np
from numbers import Number


def _is_equal_num_str_bool(elem1, elem2, tol=10e-8):
    # Compare numbers:
    are_numbers = isinstance(elem1, Number) and isinstance(elem2, Number)
    if are_numbers:
        return abs(elem1 - elem2) < tol
    else:
        try:
            np.testing.assert_equal(elem1, elem2)
        except AssertionError:
            return False
        except ValueError:
            raise NotImplementedError("Cannot compare types: {} with {}".format(
                type(elem1), type(elem2)))
        else:
            return True


def _is_list_of_dicts(item):
    return all([isinstance(e, dict) for e in item])


def _check_on_dict_keys_list(dict1, dict2):
    if not set(dict1.keys()) == set(dict2.keys()):
        return (False, "{} should be {}".format(
            sorted(set(dict1.keys())), sorted(set(dict2.keys()))))
    else:
        return True, ''


def list_to_str_summarize(lst):
    if len(lst) < 6:
        return str(lst)
    else:
        return str(lst[:3])[:-1] + ', ..., ' + str(lst[-3:])[1:]


def compare_dict(dict1, dict2, equivalent=True, msg='', tol=10e-8):
    equivalent, msg = _check_on_dict_keys_list(dict1, dict2)
    if not equivalent:
        return equivalent, msg

    for key in dict1:
        elem1 = dict1[key]
        elem2 = dict2[key]

        # Compare subdict
        if isinstance(elem1, dict) and isinstance(elem2, dict):
            tmp_equivalent, tmp_msg = compare_dict(
                elem1, elem2, equivalent=equivalent, msg=msg, tol=tol)
            equivalent = equivalent and tmp_equivalent
            msg += tmp_msg

        # Compare when list
        elif isinstance(elem1, list) and isinstance(elem2, list):

            # list of dicts:
            if _is_list_of_dicts(elem1) and _is_list_of_dicts(elem2):
                for i in range(len(elem1)):
                    tmp_equivalent, tmp_msg = compare_dict(
                        elem1[i], elem2[i],
                        equivalent=equivalent, msg=msg, tol=tol)
                    msg += tmp_msg
                    equivalent = equivalent and tmp_equivalent

            else:
                equivalent = all(
                    [_is_equal_num_str_bool(elem1[i], elem2[i], tol) for
                     i in range(len(elem1))]
                )
                if not equivalent:
                    return False, "'{}' -> {} should be {}".format(
                        key,
                        list_to_str_summarize(elem1),
                        list_to_str_summarize(elem2),
                    )

        else:
            equivalent = _is_equal_num_str_bool(elem1, elem2, tol)
            if not equivalent:
                return False, "'{}' -> {} should be {}".format(
                    key, elem1, elem2)

    return equivalent, msg


def assert_figure_equal(fig1, fig2, tol=10e-8):
    equivalent, msg = compare_dict(fig1, fig2)
    assert equivalent, msg
