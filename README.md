# Pattern-Based Collections for Blender
Categorising selections of objects within scenes is crucial for various digital content workflows. Blender gives us access to the [Collection type](https://docs.blender.org/api/current/bpy.types.Collection.html) through its Python API but lacks in tools (code and non-code) for grouping objects by common properties and metadata. This extension draws inspiration from [Pattern-Based Collections for OpenUSD](https://github.com/PixarAnimationStudios/OpenUSD-proposals/tree/main/proposals/pattern-based-collections) and is built on top of existing standards like RegEx and the JSON format to enable configuration and layering of precise sorting rules for collections in Blender.

### Some use cases
* Keep your blend-files tidy as an artist
* Divide thousands of objects into bake/export collections
* Configure model/scene variations from metadata

# Important Aspects

## Artist-friendly Configuration
Configure, test and reiterate on your collection patterns from the Blender interface
  
![rules_setup](https://github.com/user-attachments/assets/c3398a3c-0787-4dc9-9eac-8445cfb13c3e)

## JSON Export
Export and reuse your collection patterns for future projects

## Python API
```py
# Assumes you have an active collection

# Reads the json file
bpy.ops.scene.pattern_collection_import(filepath="")
bpy.ops.scene.pattern_collection_sort()  # Sorts the collection
```
## Available Sorting Categories
* Included/Excluded **Names**
* Included/Excluded **Hierarchies**
* Included/Excluded **Types**
* Included/Excluded **Materials**
* Included/Excluded **Collections**
* Included/Excluded **UV Layers**
* Included/Excluded **Attributes**

## Optimisation
The extension has the potential of sorting 1K objects in less than one second. I'm continuously searching for more optimisations; however most of the time sorting is spent on unlinking/linking of objects and cannot be parallelised.

## Additional Details
* **Enable/Disable** - Toggle its impact on sorting without completely removing it
* **Case Sensitivity** - Determines if the item is processed as case-sensitive
* **Anchor** - An item's relationship to the candidates
  * (Match, Contains, Starts with, Ends with, Match Rgx, Search Rgx, Greater, Less)
* **Reserved Attribute Names**
  * **triangles** (alt. tris) - The object's number of triangles (0 for non-meshes)
  * **bounding_box** (alt. bbox) - The object's bounding box volume (0 for non-meshes)
  * **surface_area** (alt. area) - The object's surface area (0 for non-meshes)
    * (These can be mixed, e.g., use tris/area to sort by triangle density)

### Automatic Sorting
Define your working structure *once* and let objects be categorised as you create
  
![automatic_sorting](https://github.com/user-attachments/assets/2c35a410-6f09-4401-9851-1e3d90fa5f15)

## Potential plans for the distant Future 🚀
* Core changes  
  * More generic support for object properties
  * UI Overhaul
* Quality-of-Life improvements
  * Clear/reset the pattern of a collection
  * Copying/Pasting of patterns between collections
  * Collection Pattern Presets
  * Ability to hide sorting categories not in use
  * Exclude objects from sorting
  * Sort all collections at once (and sort order)