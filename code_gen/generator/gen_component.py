"""
Methods to generate content in src/*_component.py
"""

from telnetlib import STATUS
from typing import Dict
from code_gen.generator.utils import (
    camel_to_snake,
    get_class_names,
    get_crd_info,
    parse_crd,
    snake_to_camel,
    write_snippet_to_file,
)


def get_do_paramaters_snippet(_output_src_dir, _crd_name, _crd_info):

    group, version, plural, namespace = _crd_info

    _snippet = """
        self.group = "%s"
        self.version = "%s"
        self.plural = "%s"
        self.namespace = "%s"

        self.job_request_outline_location = (
            "%s"
        )
        self.job_request_location = (
            "%s"
        )""" % (
        group,
        version,
        plural,
        namespace,
        _output_src_dir + _crd_name + "_request.yaml.tpl",
        _output_src_dir + _crd_name + "_request.yaml",
    )

    return _snippet


def get_output_prep_snippet(_output_statuses):

    _snippet = ""

    for key in _output_statuses:

        _snippet += """
        outputs.%s = str(
            ack_statuses["%s"]
            if "%s" in ack_statuses
            else None
        )""" % (
            camel_to_snake(key),
            key,
            key,
        )

    return _snippet
