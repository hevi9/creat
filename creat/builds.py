from __future__ import annotations

#
# MAKE_ITEM_MAP = {
#     "shell": Shell,
#     "use": Use,
#     "remove": Remove,
#     "copy": Copy,
#     "move": Move,
# }
#
#
# yaml = YAML()
#
#
# class Top:
#     pass
#
#
# def build(roots: List[Path], ignores: List[str]) -> Index:
#     locations = discover(roots, ignores)
#     dicts = [load(location) for location in locations]
#     toplevels = [schema.File(**d) for d in dicts]
#
#


#
#
# def load(location: Location) -> Dict[str, Any]:
#     return yaml.load(location.path)
#
#
# def build_toplevel(data: schema.File):
#     pass
#
#
# def make_source_from_dict(item: dict, location: Location) -> Source:
#     """Make source from given source control dict."""
#     source = Source(
#         name=item["source"],
#         control=item,
#         location=location,
#     )
#     make_list = item["make"]
#     for make_item in make_list:
#         if isinstance(make_item, str):
#             make_item = {"shell": make_item}
#         elif isinstance(make_item, dict):
#             pass  # NOSONAR
#         else:
#             raise TypeError(f"Invalid make item type {type(make_item)}")
#         make_type = make_item.keys() & MAKE_ITEM_MAP.keys()
#         if len(make_type) < 1:
#             raise ValueError(
#                 f"""Unknown make type in item {make_item} in {location},
#                 available make types {MAKE_ITEM_MAP.keys()}"""
#             )
#         if len(make_type) > 1:
#             raise ValueError(f"Conflicting make types {make_type}")
#         make_type = make_type.pop()
#         source.make.append(MAKE_ITEM_MAP[make_type](source, make_item))  # type: ignore
#
#     return source
#
#
# def make_sources_from_file_yaml(location: Location) -> Iterable[Source]:
#     """Make source item from yaml file."""
#     console = get_console()
#     with location.path.open() as fo:
#         text = fo.read()
#         if text.strip() == "":
#             console.print(f"{location} is empty, ignoring")
#             return
#         data = strictyaml.load(text, label=str(location.path)).data
#         if not isinstance(data, list):
#             raise TypeError(f"Top content is not a list type: '{text}': {location}")
#         for item in data:
#             yield make_source_from_dict(item, location)
#
#
# def find_mk_sources_from_roots(
#     mkroots: Iterable[Path],
#     ignores: Iterable[str],
# ) -> Iterable[Source]:
#     """Build sources from mk files in gives mk roots.
#
#     Top level function.
#     """
#     for location in discover(mkroots, ignores):
#         yield from make_sources_from_file_yaml(location)
#
#
# def update_index_from_roots(
#     index: Index,
#     roots: Iterable[Path],
#     ignore: Iterable[str],
# ) -> None:
#     """Update index sources from given root paths. Ignore given
#     ignore patterns in tree traversing.
#
#     :param index: Index to update.
#     :param roots: Directory root paths to traverse and seek sources.
#     :param ignore:  ignore patterns to ignore in tree traversing.
#     """
#     for source in find_mk_sources_from_roots(roots, ignore):
#         index.add_source(source)
#     for source in index.sources:
#         source.update(index)
