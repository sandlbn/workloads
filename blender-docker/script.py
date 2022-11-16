import bpy
import sys
import os

argv = sys.argv
argv = argv[argv.index("--") + 1:]
print(argv)

params = {}
if len(argv) > 0 and argv[0] != "":
    for pair in argv[0].split(","):
        [k,v] = pair.split(":")
        params[k] = v
print(params)

isGpu = False
if os.getenv('NVIDIA_VISIBLE_DEVICES') != None:
    isGpu = True

cycles_prefs = bpy.context.preferences.addons["cycles"].preferences

def configure_gpu():
    for scene in bpy.data.scenes:
        scene.cycles.device = 'GPU'
        scene.render.engine = 'CYCLES'

    # Set the device_type
    cycles_prefs.compute_device_type = "OPTIX"
    if "compute_device_type" in params:
        cycles_prefs.compute_device_type = params["compute_device_type"]

    # Set the device and feature set
    bpy.context.scene.cycles.device = "GPU"

    # get_devices() to let Blender detects GPU device
    cycles_prefs.get_devices()
    print(cycles_prefs.compute_device_type)
    for d in cycles_prefs.devices:
        #This is unnecessary use all devices?
        d["use"] = False
        if d["type"] == 0: #cpu
            d["use"] = True
        if d["type"] == 1: #cuda
            d["use"] = True
        if d["type"] == 3: #optix
            d["use"] = True
        print(d["type"], d["name"], d["use"])

if isGpu:
    configure_gpu()

bpy.ops.wm.open_mainfile(filepath="source.blend", load_ui=False)

if isGpu:
    bpy.context.scene.cycles.device = "GPU"
bpy.context.scene.render.engine = "CYCLES"

if "samples" in params:
    bpy.context.scene.cycles.samples = int(params["samples"])
if "fps" in params:
    bpy.context.scene.render.fps = int(params["fps"])
if "fps_base" in params:
    bpy.context.scene.render.fps = int(params["fps_base"])
if "resolution_x" in params:
    bpy.context.scene.render.resolution_x = int(params["resolution_x"])
if "resolution_y" in params:
    bpy.context.scene.render.resolution_y = int(params["resolution_y"])
if "frame_start" in params:
    bpy.context.scene.frame_start = int(params["frame_start"])
if "frame_end" in params:
    bpy.context.scene.frame_end = int(params["frame_end"])
if "frame_step" in params:
    bpy.context.scene.frame_step = int(params["frame_step"])

bpy.context.scene.render.threads_mode = "FIXED"
bpy.context.scene.render.threads = int(os.getenv('NPROC', "2"))

bpy.context.scene.render.image_settings.file_format = 'PNG'
if "animation" in params:
    print("output animation")
    bpy.context.scene.render.filepath = "/output/out_####"
else:
    print("output single image")
    bpy.context.scene.render.filepath = f'/output/out_{bpy.context.scene.frame_end}'

if "animation" in params:
    bpy.ops.render.render(animation = True)
else:
    bpy.ops.render.render(write_still = True)

