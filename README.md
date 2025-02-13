# Pattern-Based Collections for Blender
Categorizing selections of objects within scenes is essential for various digital content workflows. Blender already provides an API schema, [bpy.types.Collection](https://docs.blender.org/api/current/bpy.types.Collection.html) to do this, but is lacking in tools (code and non-code) to find and collect objects by common properties and metadata. This extension draws inspiration from [Pattern-Based Collections for OpenUSD](https://github.com/PixarAnimationStudios/OpenUSD-proposals/tree/main/proposals/pattern-based-collections) and is built on top of existing standards like RegEx and the JSON format to 1) be easy to integrate by pipeline developers into existing pipelines; and 2) be usable by Blender users without code knowledge.  
  
Below are some of the extension's most important philosophies
## Artist-friendly Configuration
Configure, test and reiterate on your collection patterns from the Blender interface
  
![rules_setup](https://github.com/user-attachments/assets/c3398a3c-0787-4dc9-9eac-8445cfb13c3e)
## JSON Export
Export and reuse your collection patterns for future projects
## Python API
```py
# Assumes you have an active collection

bpy.ops.collection.import_pattern(filepath="")  # Reads the json file
bpy.ops.collection.pattern_sort()  # Sorts the collection
```
## Automatic Sorting
Define your working structure *once* and let objects be categorised on the fly
  
![automatic_sorting](https://github.com/user-attachments/assets/2c35a410-6f09-4401-9851-1e3d90fa5f15)
## Available Sorting Categories
* Included/Excluded **Names**
* Included/Excluded **Hierarchies**
* Included/Excluded **Types**
* Included/Excluded **Materials**
* Included/Excluded **Collections**
* Included/Excluded **UV Layers**
* Included/Excluded **Attributes**
## Additional Details
* **Enable/Disable** - Toggle its impact on sorting without completely removing it
* **Case Sensitivity** - Determines if the item is processed as case-sensitive
* **Anchor** - An item's relationship to the candidates
  * (Match, Contains, Starts with, Ends with, Match Rgx, Search Rgx, Greater, Less)
* **Reserved Attribute Names**
  * **triangles** (alt. tris) - The object's number of triangles (0 for non-meshes)
  * **bounding_box** (alt. bbox) - The object's bounding box volume (0 for non-meshes)
  * **surface_area** (alt. area) - The object's surface area (0 for non-meshes)
    * (These can be mixed, e.g., use `tris/area` to sort by triangle density)
## Ideas for the Future
* QOL improvements
  * Clear Collection Pattern
  * Copy/Paste Collection Patterns between collections
  * Collection Pattern Presets
  * Exclude objects from sorting