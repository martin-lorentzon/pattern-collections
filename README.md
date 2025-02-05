# Pattern-Based Collections for Blender
Categorizing selections of objects within scenes is essential for various digital content workflows. Blender already provides an API schema, [bpy.types.Collection](https://docs.blender.org/api/current/bpy.types.Collection.html) to do this, but is lacking in tools (code and non-code) to find objects by common properties and metadata. This extension draws inspiration from [Pattern-Based Collections for OpenUSD](https://github.com/PixarAnimationStudios/OpenUSD-proposals/tree/main/proposals/pattern-based-collections) and makes use of existing syntax such as RegEx and JSON together with a custom graphical user interface to 1) be familiar to pipeline developers and 2) be usable by Blender users without code knowledge.  
  
You can find the extension's key features below ↓
## Automatic Sorting
Zero stressful outliner management while creating: let the extension take over by enabling automatic sorting
  
![automatic_sorting](https://github.com/user-attachments/assets/2c35a410-6f09-4401-9851-1e3d90fa5f15)
## User-friendly Configuration
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
<img src="https://github.com/user-attachments/assets/9a4ff9fc-cd48-455b-bdb6-71fe38003160" width="467"/>
