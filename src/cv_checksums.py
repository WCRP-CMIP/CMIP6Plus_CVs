"""
Tools for adding and validating checksums
"""
from copy import copy, deepcopy
import hashlib
import json


def calculate_checksum(dictionary, overwrite=True, checksum_location='version_metadata'):
    """
    Calculate the checksum for dictionary and add it to the Header

    Parameters
    ----------
    dictionary: dict
        The dictionary to set the checksum for.
    overwrite: bool
        Overwrite the existing checksum (default True).
    checksum_location: str
        sub-dictionary to look for in /add the checksum to.

    Raises
    ------
    RuntimeError
        If the ``checksum`` key already exists and ``overwrite`` is
        False.
    """
    if 'checksum' in dictionary['Header'][checksum_location]:
        if not overwrite:
            raise RuntimeError('Checksum already exists.')
        del dictionary['Header'][checksum_location]['checksum']
    checksum = _checksum(dictionary)
    dictionary['Header'][checksum_location]['checksum'] = checksum


def validate_checksum(dictionary, checksum_location='version_metadata'):
    """
    Validate the checksum in the ``dictionary``.

    Parameters
    ----------
    dictionary: dict
        The dictionary containing the ``checksum`` to validate.
    checksum_location: str
        sub-dictionary to look for in /add the checksum to.

    Raises
    ------
    KeyError
        If the ``checksum`` key does not exist.
    RuntimeError
        If the ``checksum`` value is invalid.
    """
    if 'checksum' not in dictionary[checksum_location]:
        raise KeyError('No checksum to validate')
    dictionary_copy = deepcopy(dictionary)
    del dictionary_copy[checksum_location]['checksum']
    checksum = _checksum(dictionary_copy)
    if dictionary[checksum_location]['checksum'] != checksum:
        msg = ('Expected checksum   "{}"\n'
               'Calculated checksum "{}"').format(dictionary[checksum_location]['checksum'],
                                                  checksum)
        raise RuntimeError(msg)


def _checksum(obj):
    obj_str = json.dumps(obj, sort_keys=True)
    checksum_hex = hashlib.md5(obj_str.encode('utf8')).hexdigest()
    return 'md5: {}'.format(checksum_hex)