"""
jpipe_runner.utils
~~~~~~~~~~~~~~~~~~

This module contains the utilities of jPipe Runner.
"""

import json
import re


def unquote_string(s: str) -> str:
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        raise ValueError(f'{repr(s)} is not a valid STRING') from e


def sanitize_string(s: str) -> str:
    # Convert to snake case
    # Ref: https://stackoverflow.com/a/1176023/9243111
    s = re.sub(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', '_', s).lower()
    # Use re to keep only allowed characters.
    sanitized = re.sub(r'[^a-z0-9_]', '',
                       re.sub(r'\s+', '_',
                              re.sub(r'[/|\\]', ' ', s).strip()))
    return sanitized


def _test():
    """test unquote_string"""
    assert unquote_string('"hello"') == 'hello'
    try:
        unquote_string("'hello'")
    except ValueError:
        pass

    """test sanitize_string"""
    assert sanitize_string('Hello,              world!') == 'hello_world'
    assert sanitize_string('Check contents w.r.t. NDA ') == 'check_contents_wrt_nda'
    assert sanitize_string('Check PEP8 coding standard') == 'check_pep8_coding_standard'
    assert sanitize_string('Check        Grammar/Typos') == 'check_grammar_typos'
    assert sanitize_string('Check is valid HTTPHeader ') == 'check_is_valid_http_header'
    assert sanitize_string('Check enabled PodDisruptionBudget') == 'check_enabled_pod_disruption_budget'


if __name__ == "__main__":
    _test()
