# LogoutSkips

## Acknowledgements
- Zarant: Logout skip locations
- Tactics and TommySalami: Logout skips discoveries and research; consulting
- Semlar: Original library for drawing lines on map

## Notes
This addon is experimental; don't rely on the logout skip locations too much.  To use this addon, open the map and click the `Show LogoutSkips` button.  Red `x`'s are locations where the logout skips will teleport you to. The red lines are Voronoi partitions which act as boundaries between different logout skip teleport locations.  The idea is that if you perform a logout skip, you will be teleported to the location indicated by the `x` that is within the polygon that you are in.

## Special Mechanics

### Season of Discovery Remnants
SoD included new graveyards and instances that are now on non-SoD servers

### Special Subzones
For both Unstuck and Death skips there are special rules involving different subzones:

* Death Skips (`death_subzone_boundaries.json`):
   - you do not get teleported to these special subzones if you are outside of it
   - mainly starting zones, but some more elsewhere     
* Unstuck Skips (`unstuck_subzone_boundaries.json`):
   - you do not get teleported to these special subzones if you are outside of it     
   - only aware of one for now - The Gurubashi Arena
      * CAREFUL - this will kill you by spawning you very high in the air

## Contributing
This project uses the locations of graveyards and instance portals (located in `gyClassic.json` and `instances.json`) and it converts those json files into usable lua files for an addon in WoW classic.  the generated files (located in the `Data/` directory) includes locations for instances and graveyards as well as a partitions file that indicates voronoi lines used to draw lines on the map. 

The generated partition files contain a Lua table of line segments representing Voronoi diagram edges. Each entry in the table is a 4-element array:
-    {x1, y1, x2, y2}
Where:
x1, y1 = Start point of the line segment (in world coordinates)
x2, y2 = End point of the line segment (in world coordinates)

to run the program that generates the data points:
```
python GenerateVoronoiPartitions.py
```
