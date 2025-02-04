# Pattern Collections for Blender
Organize your Blender scene with Pattern Collections, designed to bring structure and automation to your pipeline.  
Define precise rules for how objects are categorized, reducing manual sorting and streamlining your use of the outliner.

### Some use cases
* Keeping your blend-files tidy as an artist
* Sorting literally thousands of objects into bake collections
* Spotting small, big or highly dense geometries in your pipeline

## Automatic Sorting
Design away without constantly managing a cluttered outliner by turning on automatic sorting
  
![automatic_sorting](https://github.com/user-attachments/assets/2c35a410-6f09-4401-9851-1e3d90fa5f15)

## Lightning fast Configuration
Configuring, testing and reiterating on sorting patterns is fast and requires minimal effort
  
![rules_setup](https://github.com/user-attachments/assets/11459530-66b9-4549-abdb-ec03a43f8276)

## JSON Export
Export and reuse your sorting patterns for future projects ⭐

## Python API
```py
context.collection = bpy.data.collections.new(name="New Pattern Collection")

bpy.ops.collection.import_pattern(filepath="")  # Reads the json file
bpy.ops.collection.pattern_sort()
```

## More Details
<details>
<summary>Sorting Categories</summary>

### Currently Available Sorting Categories

* Included.../Excluded **Names**
* Included.../Excluded **Hierarchies**
* Included.../Excluded **Types**
* Included.../Excluded **Materials**
* Included.../Excluded **Collections**
* Included.../Excluded **UV Layers**
* Included.../Excluded **Attributes**
</details>

<details>
<summary>Common Rules</summary>

### A rule (or item) in any category has the implemented functionalities-

* **Enable/Disable** - Toggle its impact on sorting without completely removing it  
* **Case Sensitivity** - Determines if the item is processed as case-sensitive  
* **Anchor** - An item's relationship to the candidates
  * (Match, Contains, Starts with, Ends with, Match Rgx, Search Rgx)  
</details>

<details>
<summary>Attributes and Metadata</summary>
  
### Rules in the attribute category have added features to better utilise metadata
  
* Two more anchors - (**Greater Than, Less Than**) (For numeric values)
* Reserved attribute names  
  * **triangles** (shorthand: tris) - The object's number of triangles (0 for non-meshes)
  * **bounding_box** (shorthand: bbox) - The object's bounding box volume (0 for non-meshes)
  * **surface_area** (shorthand: area) - The object's surface area (0 for non-meshes)
    * (These can be mixed, e.g., use **tris/area** to sort by triangle density)
---
![attributes_demo](https://github.com/user-attachments/assets/1a6f9114-6598-45cc-9626-4f8542afffcd)
</details>

