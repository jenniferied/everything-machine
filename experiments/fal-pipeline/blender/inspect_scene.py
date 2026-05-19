"""Headless Blender script: dump scene info for EA template."""
import bpy

scene = bpy.context.scene
print("=== SCENE ===")
print(f"name: {scene.name}")
print(f"frame range: {scene.frame_start}-{scene.frame_end} ({scene.frame_end - scene.frame_start + 1} frames)")
print(f"fps: {scene.render.fps}/{scene.render.fps_base} = {scene.render.fps / scene.render.fps_base:.2f}")
print(f"resolution: {scene.render.resolution_x} x {scene.render.resolution_y} ({scene.render.resolution_percentage}%)")
print(f"engine: {scene.render.engine}")
print(f"active camera: {scene.camera.name if scene.camera else 'None'}")
print()

print("=== CAMERAS ===")
for obj in bpy.data.objects:
    if obj.type == 'CAMERA':
        c = obj.data
        print(f"  {obj.name} | loc {tuple(round(v,2) for v in obj.location)} | rot_eul {tuple(round(v,2) for v in obj.rotation_euler)}")
        print(f"    focal: {c.lens}mm | sensor: {c.sensor_width}x{c.sensor_height} | clip {c.clip_start}-{c.clip_end}")
        # constraints
        for con in obj.constraints:
            print(f"    constraint: {con.type} -> {getattr(con, 'target', None)}")
print()

print("=== OBJECTS (top-level) ===")
for obj in bpy.data.objects:
    parent = obj.parent.name if obj.parent else '-'
    print(f"  {obj.type:8s} {obj.name:40s} parent={parent}")
print()

print("=== COLLECTIONS ===")
for coll in bpy.data.collections:
    print(f"  {coll.name}: {len(coll.objects)} obj, {len(coll.children)} children")
