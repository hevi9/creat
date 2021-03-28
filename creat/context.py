""" Managing jinja2 vars context. """

from typing import Any, Mapping

import jinja2

env = jinja2.Environment(  # nosec
    variable_start_string="${",
    variable_end_string="}",
    undefined=jinja2.StrictUndefined,
)


def render(text: str, context: Mapping[str, Any]) -> str:
    """ Render text block with context. """
    tmpl = jinja2.Template.from_code(
        environment=env,
        code=env.compile(text, filename="internal"),
        globals=env.make_globals({}),
        uptodate=None,
    )
    return tmpl.render(context)


def make_root_context(target_name: str) -> Mapping[str, Any]:
    """ Make root context. """
    return {
        "name": target_name,
        "target": target_name,
    }
