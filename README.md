# Pattern Collections for Blender
Pattern-based Collection Sorting allows for precise control over how our scenes are organised.  
Each collection holds its own pattern, a ruleset describing which objects to collect and those to leave out.

### We can utilise the currently implemented sorting categories ### 
* Included.../Excluded Names
* Included.../Excluded Hierarchies
* Included.../Excluded Types
* Included.../Excluded Materials
* Included.../Excluded Collections
* Included.../Excluded UV Layers
* Included.../Excluded Attributes

### A rule (or item) in each category has the implemented functionalities ###
* **Enable/Disable** - Toggle its impact on sorting without completely removing it
* **Case Sensitivity** - Determines if the item is processed as case-sensitive
* **Anchor** - (Match, Contains, Starts with, Ends with, Match Regex, Search Regex)

### Attribute rules have a couple of additional features ###
* Two more anchors - (**Greater Than, Less Than**) (For numeric values)
* Reserved property names  
  * **triangles** (shorthand: tris) - The object's number of triangles (0 for non-meshes)
  * **bounding_box** (shorthand: bbox) - The object's bounding box (0 for non-meshes)
  * **surface_area** (shorthand: area) - The object's surface area (0 for non-meshes)
    * (These can be mixed into **tris/area** e.g. to sort by the objects' triangle density)

### Automatic Sorting
TODO:
