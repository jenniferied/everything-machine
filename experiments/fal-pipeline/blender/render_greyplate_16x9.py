"""Render the EA template at 16:9 landscape as a greyplate motion reference.

Camera position/animation is preserved — only the output frame is reshaped from
9:16 portrait to 16:9 landscape. The camera sensor is flipped to landscape
(36 x 20.25mm) so the same focal length yields a sensible landscape framing.
"""
import bpy
import sys
import os

# CLI args after `--` separator
argv = sys.argv
out_dir = argv[argv.index("--") + 1] if "--" in argv else "/tmp/ea_render"
os.makedirs(out_dir, exist_ok=True)

scene = bpy.context.scene
print(f"[render] before: res {scene.render.resolution_x}x{scene.render.resolution_y}, engine {scene.render.engine}")

# 1) 16:9 landscape resolution
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100

# 2) Camera sensor: portrait 36x64 -> landscape 36x20.25 (keeps width, 16:9 ratio)
cam_data = scene.camera.data
print(f"[render] camera was sensor {cam_data.sensor_width}x{cam_data.sensor_height}, fit {cam_data.sensor_fit}")
cam_data.sensor_fit = 'HORIZONTAL'
cam_data.sensor_width = 36.0
cam_data.sensor_height = 36.0 * 9 / 16   # 20.25

# 3) Use EEVEE_NEXT (fast, gives a clean clay-style look out of the box)
try:
    scene.render.engine = 'BLENDER_EEVEE_NEXT'
except Exception:
    scene.render.engine = 'BLENDER_EEVEE'
print(f"[render] engine -> {scene.render.engine}")

# 4) Output: MP4 directly (scene is preset to FFMPEG, keep it)
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'HIGH'
scene.render.filepath = os.path.join(out_dir, "ea_greyplate_16x9.mp4")

# 5) Render all frames
print(f"[render] frames {scene.frame_start}..{scene.frame_end} -> {out_dir}")
bpy.ops.render.render(animation=True)
print("[render] done")
