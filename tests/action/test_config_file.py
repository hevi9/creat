""" Test config file updating. """

import pytest


@pytest.mark.skip(reason="TODO")
def test_config_file(mkroot):
    """ Test updating json file. """
    mkroot.have(
        "test/source/make_cmd.mk.yaml",
        """
        -   source: config_file
            make:
            -   config-file: ${target}/tsconfig.json
                value:
                    compilerOptions:
                        module: es6
        """,
    )
