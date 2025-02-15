"""
This module defines the configurable properties for every kind of sorting-category item 
"""

import bpy


#fmt: off
class BaseItemPropertyGroup(bpy.types.PropertyGroup):
    """
    "Base" covers all sorting-categories that dont need anything extra
    """
    anchor_enum_items = [
        ("MATCH",  "Match",    "Candidate matches the pattern"),
        ("SLICE",  "Contains", "Candidate contains the pattern"),
        ("PREFIX", "Starts with", "Pattern occurs at the beginning of the candidate"),
        ("SUFFIX", "Ends with",   "Pattern occurs at the end of the candidate"),
        ("REGEX_MATCH", "Match Rgx",   "Candidate matches the pattern\n(Uses regular expressions)"),
        ("REGEX_SEARCH", "Search Rgx", "Candidate contains the pattern\n(Uses regular expressions)")]

    anchor: bpy.props.EnumProperty(
        name="Anchor",
        description="Anchor Type",
        items=anchor_enum_items,
        default="MATCH"
        )

    case_sensitive: bpy.props.BoolProperty(
        name="Case Sensitivity",
        description="Determines if the item is processed as case-sensitive",
        default=True
        )

    enable: bpy.props.BoolProperty(
        name="Enable",
        description="Determines if the item has an effect on sorting",
        default=True
        )


class AttributeItemPropertyGroup(BaseItemPropertyGroup):
    """
    "Attribute" covers custom attributes which require more math-functionality
    """
    anchor_enum_items = [
        ("MATCH",  "Match",    "Candidate matches the pattern"),
        ("SLICE",  "Contains", "Candidate contains the pattern"),
        ("PREFIX", "Starts with", "Pattern occurs at the beginning of the candidate"),
        ("SUFFIX", "Ends with",   "Pattern occurs at the end of the candidate"),
        ("REGEX_MATCH", "Match Rgx",   "Candidate matches the pattern\n(Uses regular expressions)"),
        ("REGEX_SEARCH", "Search Rgx", "Candidate contains the pattern\n(Uses regular expressions)"),
        ("GREATER_THAN", "Greater",   "Candidate is greater than the pattern\n(Numerical)"),
        ("LESS_THAN",    "Less",      "Candidate is less than the pattern\n(Numerical)")]

    anchor: bpy.props.EnumProperty(
        name="Anchor",
        description="Anchor Type",
        items=anchor_enum_items,
        default="MATCH"
        )

    value: bpy.props.StringProperty(
        name="Value",
        description="The value of the attribute",
        default=""
        )
# fmt: on