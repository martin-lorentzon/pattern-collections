"""
This module defines the logic responsible for sorting of scene objects.
"""

import bpy
from . import utils
import re
from typing import Tuple
from bpy.types import PropertyGroup


sorting_timers = {}


def match_candidate(pattern: str, anchor: str, candidate, case_sensitive) -> bool:
    if anchor in ["GREATER_THAN", "LESS_THAN"]:
        try:
            pattern = float(pattern)
            candidate = float(candidate)
        except ValueError: return False
    else:
        pattern = str(pattern)
        candidate = str(candidate)

        if not case_sensitive and anchor not in ["REGEX_MATCH", "REGEX_SEARCH"]:
            pattern = pattern.lower()
            candidate = candidate.lower()

    match anchor:
        case "MATCH":
            if pattern == candidate:
                return True
        case "SLICE":
            if pattern in candidate:
                return True
        case "PREFIX":
            if candidate.startswith(pattern):
                return True
        case "SUFFIX":
            if candidate.endswith(pattern):
                return True
        case "REGEX_MATCH":
            if re.match(pattern, candidate):
                return True
        case "REGEX_SEARCH":
            if re.search(pattern, candidate):
                return True
        case "GREATER_THAN":
            if candidate > pattern:
                return True
        case "LESS_THAN":
            if candidate < pattern:
                return True
    return False


def test_category(properties: PropertyGroup, sorting_category: str, candidates: list) -> bool:
    items  = getattr(properties, sorting_category)
    invert = True if sorting_category.startswith("excluded") else False

    if not items or all(not item.enable for item in items):
        return True

    for item in [i for i in items if i.enable]:
        for candidate in candidates:
            matched = match_candidate(item.name, item.anchor, candidate, item.case_sensitive)

            if matched:
                return False if invert else True
    return True if invert else False


def test_category_attribute(properties: PropertyGroup, sorting_category: str, ob_attributes: dict, ob: bpy.types.Object) -> bool:
    items  = getattr(properties, sorting_category)
    invert = True if sorting_category.startswith("excluded") else False

    if not items or all(not item.enable for item in items):
        return True

    for item in [i for i in items if i.enable]:
        match item.name:
            case "triangles" | "tris":
                candidate = utils.triangle_count(ob)
            case "bounding_box" | "bbox":
                candidate = utils.volume(ob)
            case "surface_area" | "area":
                candidate = utils.surface_area(ob)
            case "triangles/bounding_box" | "tris/bbox" | "triangles/bbox" | "tris/bounding_box":
                try:
                    triangles = utils.triangle_count(ob)
                    bounding_box = utils.volume(ob)
                    candidate = triangles / bounding_box
                except ZeroDivisionError:
                    candidate = 0
            case "triangles/surface_area" | "tris/area" | "triangles/area" | "tris/surface_area":
                try:
                    triangles = utils.triangle_count(ob)
                    surface_area = utils.surface_area(ob)
                    candidate = triangles / surface_area
                except ZeroDivisionError:
                    candidate = 0
            case _:
                candidate = ob_attributes.get(item.name, "")  # Default behaviour

        matched = match_candidate(item.value, item.anchor, candidate, item.case_sensitive)

        if matched:
            return False if invert else True
    return True if invert else False


def sort_objects(collection, objects: list[bpy.types.Object]) -> list[Tuple[bpy.types.Collection, list[bpy.types.Object], bool]]:
    sorting_commands = []

    properties = collection.pattern_collection_properties
    link_objects = []
    unlink_objects = []

    for ob in objects:
        candidates = [ob.name]
        name_green = test_category(properties, "included_names", candidates) and \
                     test_category(properties, "excluded_names", candidates)

        candidates = [p.name for p in utils.all_parents(ob)]
        hierarchies_green = test_category(properties, "included_hierarchies", candidates) and \
                            test_category(properties, "excluded_hierarchies", candidates)

        candidates = [ob.type]
        type_green = test_category(properties, "included_types", candidates) and \
                     test_category(properties, "excluded_types", candidates)

        candidates = [mat.name for mat in getattr(ob.data, "materials", [])]
        materials_green = test_category(properties, "included_materials", candidates) and \
                          test_category(properties, "excluded_materials", candidates)

        candidates = [col.name for col in ob.users_collection]
        collections_green = test_category(properties, "included_collections", candidates) and \
                            test_category(properties, "excluded_collections", candidates)

        candidates = [uv_layer.name for uv_layer in getattr(ob.data, "uv_layers", [])]
        uv_layers_green = test_category(properties, "included_uv_layers", candidates) and \
                          test_category(properties, "excluded_uv_layers", candidates)

        candidates = {attribute: value for attribute, value in ob.items()}
        attributes_green = test_category_attribute(properties, "included_attributes", candidates, ob) and \
                           test_category_attribute(properties, "excluded_attributes", candidates, ob)

        link = name_green and \
                hierarchies_green and \
                type_green and \
                materials_green and \
                collections_green and \
                uv_layers_green and \
                attributes_green

        already_in_collection = ob.name in collection.objects

        if link != already_in_collection:
            if link:
                link_objects.append(ob)
            else:
                unlink_objects.append(ob)

    if len(link_objects) > 0:
        sorting_commands.append((collection, link_objects, True))

    if len(unlink_objects) > 0:
        sorting_commands.append((collection, unlink_objects, False))
    return sorting_commands


def process_sorting_commands(sorting_commands: list[Tuple[bpy.types.Collection, list[bpy.types.Object], bool]]) -> None:
    for col, objects, link in sorting_commands:
            for ob in objects:
                if link:
                    col.objects.link(ob)
                else:
                    col.objects.unlink(ob)
    return None