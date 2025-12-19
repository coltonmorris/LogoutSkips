from Voronoi import Voronoi
import os
import json
from pathlib import Path

file_path = os.path.dirname(os.path.realpath(__file__))

def toLua(input_string):
    output_string = input_string.replace('[', '{')
    output_string = output_string.replace(']', '}')
    output_string = output_string.replace(')', '}')
    output_string = output_string.replace('(', '{')
    return output_string

def polygon_to_line_segments(points):
    """Convert a list of polygon points to line segments (closing the polygon)"""
    segments = []
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]  # Wrap around to close the polygon
        segments.append((p1[0], p1[1], p2[0], p2[1]))
    return segments

def line_to_dashes(x1, y1, x2, y2, dash_length=40, gap_length=25):
    """Break a line segment into dashes with gaps"""
    import math
    dx = x2 - x1
    dy = y2 - y1
    line_length = math.sqrt(dx*dx + dy*dy)

    if line_length == 0:
        return []

    # Normalize direction
    nx = dx / line_length
    ny = dy / line_length

    dashes = []
    pos = 0
    is_dash = True

    while pos < line_length:
        if is_dash:
            end_pos = min(pos + dash_length, line_length)
            dash_x1 = x1 + nx * pos
            dash_y1 = y1 + ny * pos
            dash_x2 = x1 + nx * end_pos
            dash_y2 = y1 + ny * end_pos
            dashes.append((dash_x1, dash_y1, dash_x2, dash_y2))
            pos = end_pos
        else:
            pos += gap_length
        is_dash = not is_dash

    return dashes

def polygon_to_dashed_segments(points, dash_length=40, gap_length=25):
    """Convert polygon to dashed line segments"""
    all_dashes = []
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]
        dashes = line_to_dashes(p1[0], p1[1], p2[0], p2[1], dash_length, gap_length)
        all_dashes.extend(dashes)
    return all_dashes

f = open('gyClassic.json')
gy_locs = json.load(f)
f.close()

# Load subzone boundaries (for death skips)
f = open('death_subzone_boundaries.json')
death_subzone_boundaries = json.load(f)
f.close()

# Load unstuck subzone boundaries (for unstuck skips)
f = open('unstuck_subzone_boundaries.json')
unstuck_subzone_boundaries = json.load(f)
f.close()

kalimdor_locs_set = set()
kalimdor_gy_locs_set = set()
kalimdor_locs = []
kalimdor_gy_locs = []

for v in gy_locs['1']:
    if (v['x'], v['y']) not in kalimdor_locs_set:
        kalimdor_locs_set.add((v['x'],v['y']))
        kalimdor_locs.append((v['x'],v['y'], v['title']))
    if 'graveyard' in v and v['graveyard'] == 1:
        if (v['x'], v['y']) not in kalimdor_gy_locs_set:
            kalimdor_gy_locs_set.add((v['x'], v['y']))
            kalimdor_gy_locs.append((v['x'],v['y'], v['title']))

eastern_kingdom_locs_set = set()
eastern_kingdom_gy_locs_set = set()
eastern_kingdom_locs = []
eastern_kingdom_gy_locs = []
for v in gy_locs['0']:
    if (v['x'], v['y']) not in eastern_kingdom_locs_set:
        eastern_kingdom_locs_set.add((v['x'],v['y']))
        eastern_kingdom_locs.append((v['x'],v['y'], v['title']))
    if 'graveyard' in v and v['graveyard'] == 1:
        eastern_kingdom_gy_locs_set.add((v['x'], v['y'], v['title']))
        if (v['x'], v['y']) not in eastern_kingdom_gy_locs_set:
            eastern_kingdom_gy_locs_set.add((v['x'], v['y']))
            eastern_kingdom_gy_locs.append((v['x'],v['y'], v['title']))

f = open('instances.json')
instance_locs = json.load(f)
f.close()

for v in instance_locs['1']:
    if (v['x'], v['y']) not in kalimdor_locs_set:
        kalimdor_locs_set.add((v['x'],v['y']))
        kalimdor_locs.append((v['x'],v['y'], v['title']))

for v in instance_locs['0']:
    if (v['x'], v['y']) not in eastern_kingdom_locs_set:
        eastern_kingdom_locs_set.add((v['x'],v['y']))
        eastern_kingdom_locs.append((v['x'],v['y'], v['title']))


p = Path('Data/eastern_kingdom_locs.lua')
p.open('w').write("eastern_kingdom_locs = " + toLua(json.dumps(eastern_kingdom_locs)))

p = Path('Data/eastern_kingdom_gy_locs.lua')
p.open('w').write("eastern_kingdom_gy_locs = " + toLua(json.dumps(eastern_kingdom_gy_locs)))

p = Path('Data/kalimdor_locs.lua')
p.open('w').write("kalimdor_locs = " + toLua(json.dumps(kalimdor_locs)))

p = Path('Data/kalimdor_gy_locs.lua')
p.open('w').write("kalimdor_gy_locs = " + toLua(json.dumps(kalimdor_gy_locs)))

vp = Voronoi(kalimdor_locs)
vp.process()
p = Path('Data/kalimdor_partitions.lua')
p.open('w').write("kalimdor_partitions = " + toLua(json.dumps(vp.get_output())))

vp = Voronoi(eastern_kingdom_locs)
vp.process()
p = Path('Data/eastern_kingdom_partitions.lua')
p.open('w').write("eastern_kingdom_partitions = " + toLua(json.dumps(vp.get_output())))

vp = Voronoi(eastern_kingdom_gy_locs)
vp.process()
p = Path('Data/eastern_kingdom_gy_partitions.lua')
p.open('w').write("eastern_kingdom_gy_partitions = " + toLua(json.dumps(vp.get_output())))

vp = Voronoi(kalimdor_gy_locs)
vp.process()
p = Path('Data/kalimdor_gy_partitions.lua')
p.open('w').write("kalimdor_gy_partitions = " + toLua(json.dumps(vp.get_output())))

# Generate subzone boundary line segments (dashed)
eastern_kingdom_subzone_lines = []
kalimdor_subzone_lines = []

if '0' in death_subzone_boundaries:
    for subzone in death_subzone_boundaries['0']:
        # Use dashed segments for visual distinction
        dashed_segments = polygon_to_dashed_segments(subzone['points'], dash_length=40, gap_length=25)
        eastern_kingdom_subzone_lines.extend(dashed_segments)

if '1' in death_subzone_boundaries:
    for subzone in death_subzone_boundaries['1']:
        # Use dashed segments for visual distinction
        dashed_segments = polygon_to_dashed_segments(subzone['points'], dash_length=40, gap_length=25)
        kalimdor_subzone_lines.extend(dashed_segments)

p = Path('Data/eastern_kingdom_subzone_lines.lua')
p.open('w').write("eastern_kingdom_subzone_lines = " + toLua(json.dumps(eastern_kingdom_subzone_lines)))

p = Path('Data/kalimdor_subzone_lines.lua')
p.open('w').write("kalimdor_subzone_lines = " + toLua(json.dumps(kalimdor_subzone_lines)))

print("Generated death skip subzone boundary lines:")
print(f"  Eastern Kingdoms: {len(eastern_kingdom_subzone_lines)} line segments")
print(f"  Kalimdor: {len(kalimdor_subzone_lines)} line segments")

# Generate unstuck skip subzone boundary line segments (dashed)
eastern_kingdom_unstuck_subzone_lines = []
kalimdor_unstuck_subzone_lines = []

if '0' in unstuck_subzone_boundaries:
    for subzone in unstuck_subzone_boundaries['0']:
        dashed_segments = polygon_to_dashed_segments(subzone['points'], dash_length=40, gap_length=25)
        eastern_kingdom_unstuck_subzone_lines.extend(dashed_segments)

if '1' in unstuck_subzone_boundaries:
    for subzone in unstuck_subzone_boundaries['1']:
        dashed_segments = polygon_to_dashed_segments(subzone['points'], dash_length=40, gap_length=25)
        kalimdor_unstuck_subzone_lines.extend(dashed_segments)

p = Path('Data/eastern_kingdom_unstuck_subzone_lines.lua')
p.open('w').write("eastern_kingdom_unstuck_subzone_lines = " + toLua(json.dumps(eastern_kingdom_unstuck_subzone_lines)))

p = Path('Data/kalimdor_unstuck_subzone_lines.lua')
p.open('w').write("kalimdor_unstuck_subzone_lines = " + toLua(json.dumps(kalimdor_unstuck_subzone_lines)))

print("Generated unstuck skip subzone boundary lines:")
print(f"  Eastern Kingdoms: {len(eastern_kingdom_unstuck_subzone_lines)} line segments")
print(f"  Kalimdor: {len(kalimdor_unstuck_subzone_lines)} line segments")

# y = json.dumps(vp.get_output())
# y = y.replace('[', '{')
# y = y.replace(']', '}')
# print("kalimdor")
# print(y)

vp = Voronoi(eastern_kingdom_locs)
vp.process()
y = json.dumps(vp.get_output())
y = y.replace('[', '{')
y = y.replace(']', '}')
print("eastern kingdom")
print(y)
