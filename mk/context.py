from typing import Any, Mapping

import jinja2

env = jinja2.Environment(  # nosec
    variable_start_string="${",
    variable_end_string="}",
    undefined=jinja2.StrictUndefined,
)


def render(text: str, context: Mapping[str, Any]) -> str:
    globals2 = env.make_globals({})
    tmpl = jinja2.Template.from_code(
        env, env.compile(text, filename="TODO:FILE"), globals2, None
    )
    return tmpl.render(context)


def make_root_context(target_name: str) -> Mapping[str, Any]:
    """ Make root context. """
    return {
        "name": target_name,
        "target": target_name,
    }
