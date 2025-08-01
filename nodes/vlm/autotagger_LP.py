import numpy as np
import csv
import os
import sys
import requests

from PIL import Image
from server import PromptServer
from aiohttp import web
import folder_paths
import json
import shutil
import inspect

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))

supported_autotaggers_extensions = set(['.onnx'])

try:
    folder_paths.folder_names_and_paths["autotaggers"] = (folder_paths.folder_names_and_paths["autotaggers"][0], supported_autotaggers_extensions)
except:
    if not os.path.isdir(os.path.join(folder_paths.models_dir, "autotaggers")):
        os.mkdir(os.path.join(folder_paths.models_dir, "autotaggers"))
        
    folder_paths.folder_names_and_paths["autotaggers"] = ([os.path.join(folder_paths.models_dir, "autotaggers")], supported_autotaggers_extensions)

config = None

def is_logging_enabled():
    config = get_extension_config()
    if "logging" not in config:
        return False
    return config["logging"]

def log(message, type=None, always=False):
    if not always and not is_logging_enabled():
        return

    if type is not None:
        message = f"[{type}] {message}"

    name = get_extension_config()["name"]

    print(f"(LevelPixel Advanced:{name}) {message}")

def get_ext_dir(subpath=None, mkdir=False):
    dir = os.path.dirname(__file__)
    if subpath is not None:
        dir = os.path.join(dir, subpath)

    dir = os.path.abspath(dir)

    if mkdir and not os.path.exists(dir):
        os.makedirs(dir)
    return dir

def get_comfy_dir(subpath=None):
    dir = os.path.dirname(inspect.getfile(PromptServer))
    if subpath is not None:
        dir = os.path.join(dir, subpath)

    dir = os.path.abspath(dir)

    return dir

def get_web_ext_dir():
    config = get_extension_config()
    name = config["name"]
    dir = get_comfy_dir("web/extensions/levelpixeladvanced")
    if not os.path.exists(dir):
        os.makedirs(dir)
    dir += "/" + name
    return dir

def get_extension_config(reload=False):
    global config
    if reload == False and config is not None:
        return config

    config_path = get_ext_dir("autotagger_LP.user.json")
    if not os.path.exists(config_path):
        config_path = get_ext_dir("autotagger_LP.json")

    if not os.path.exists(config_path):
        log("Missing autotagger_LP.json and autotagger_LP.user.json, this extension may not work correctly. Please reinstall the extension.",
            type="ERROR", always=True)
        print(f"Extension path: {get_ext_dir()}")
        return {"name": "Unknown", "version": -1}
    with open(config_path, "r") as f:
        config = json.loads(f.read())
    return config

def link_js(src, dst):
    src = os.path.abspath(src)
    dst = os.path.abspath(dst)
    if os.name == "nt":
        try:
            import _winapi
            _winapi.CreateJunction(src, dst)
            return True
        except:
            pass
    try:
        os.symlink(src, dst)
        return True
    except:
        import logging
        logging.exception('')
        return False

def is_junction(path):
    if os.name != "nt":
        return False
    try:
        return bool(os.readlink(path))
    except OSError:
        return False

def install_js():
    src_dir = get_ext_dir("web/js")
    if not os.path.exists(src_dir):
        log("No JS")
        return

    should_install = should_install_js()
    if should_install:
        log("it looks like you're running an old version of ComfyUI that requires manual setup of web files, it is recommended you update your installation.", "warning", True)
    dst_dir = get_web_ext_dir()
    linked = os.path.islink(dst_dir) or is_junction(dst_dir)
    if linked or os.path.exists(dst_dir):
        if linked:
            if should_install:
                log("JS already linked")
            else:
                os.unlink(dst_dir)
                log("JS unlinked, PromptServer will serve extension")
        elif not should_install:
            shutil.rmtree(dst_dir)
            log("JS deleted, PromptServer will serve extension")
        return
    
    if not should_install:
        log("JS skipped, PromptServer will serve extension")
        return
    
    if link_js(src_dir, dst_dir):
        log("JS linked")
        return

    log("Copying JS files")
    shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)

def should_install_js():
    return not hasattr(PromptServer.instance, "supports") or "custom_nodes_from_web" not in PromptServer.instance.supports

def init(check_imports):
    log("Init")

    if check_imports is not None:
        import importlib.util
        for imp in check_imports:
            spec = importlib.util.find_spec(imp)
            if spec is None:
                log(f"{imp} is required, please check requirements are installed.", type="ERROR", always=True)
                return False

    install_js()
    return True

def download_to_file(url, destination, is_ext_subpath=True):
    if is_ext_subpath:
        destination = get_ext_dir(destination)
    proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
    proxies = {"http": proxy, "https": proxy} if proxy else None
    response = requests.get(url, stream=True, proxies=proxies)
    response.raise_for_status()
    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size=2048):
            if chunk:
                f.write(chunk)

def update_node_status(client_id, node, text, progress=None):
    if client_id is None:
        client_id = PromptServer.instance.client_id

    if client_id is None:
        return

    PromptServer.instance.send_sync("levelpixeladvanced/update_status", {
        "node": node,
        "progress": progress,
        "text": text
    }, client_id)

async def update_node_status_async(client_id, node, text, progress=None):
    if client_id is None:
        client_id = PromptServer.instance.client_id

    if client_id is None:
        return

    await PromptServer.instance.send("levelpixeladvanced/update_status", {
        "node": node,
        "progress": progress,
        "text": text
    }, client_id)

config_autotagger = get_extension_config()

defaults = {
    "model": "wd-eva02-large-tagger-v3",
    "threshold": 0.35,
    "character_threshold": 0.85,
    "replace_underscore": False,
    "trailing_comma": False,
    "exclude_tags": "",
    "ortProviders": ["CUDAExecutionProvider", "CPUExecutionProvider"],
    "HF_ENDPOINT": "https://huggingface.co"
}
defaults.update(config_autotagger.get("settings", {}))

models_dir = folder_paths.get_folder_paths("autotaggers")[0]
if not os.path.exists(models_dir):
    os.makedirs(models_dir)

known_models = list(config_autotagger["models"].keys())

def get_installed_models():
    models = filter(lambda x: x.endswith(".onnx"), os.listdir(models_dir))
    models = [m for m in models if os.path.exists(os.path.join(models_dir, os.path.splitext(m)[0] + ".csv"))]
    return models

def tag(image, model_name, threshold=0.35, character_threshold=0.85, exclude_tags="", replace_underscore=True, trailing_comma=False, client_id=None, node=None):
    if model_name.endswith(".onnx"):
        model_name = model_name[0:-5]
    installed = list(get_installed_models())
    if not any(model_name + ".onnx" in s for s in installed):
        print(f"Started downloading model file {model_name}")
        download_model(model_name, client_id, node)
        print(f"Finished downloading model file {model_name}")

    name = os.path.join(models_dir, model_name + ".onnx")
    from onnxruntime import InferenceSession
    model = InferenceSession(name, providers=defaults["ortProviders"])

    input = model.get_inputs()[0]
    height = input.shape[1]

    # Reduce to max size and pad with white
    ratio = float(height)/max(image.size)
    new_size = tuple([int(x*ratio) for x in image.size])
    image = image.resize(new_size, Image.LANCZOS)
    square = Image.new("RGB", (height, height), (255, 255, 255))
    square.paste(image, ((height-new_size[0])//2, (height-new_size[1])//2))

    image = np.array(square).astype(np.float32)
    image = image[:, :, ::-1]  # RGB -> BGR
    image = np.expand_dims(image, 0)

    # Read all tags from csv and locate start of each category
    tags = []
    general_index = None
    character_index = None
    with open(os.path.join(models_dir, model_name + ".csv")) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if general_index is None and row[2] == "0":
                general_index = reader.line_num - 2
            elif character_index is None and row[2] == "4":
                character_index = reader.line_num - 2
            if replace_underscore:
                tags.append(row[1].replace("_", " "))
            else:
                tags.append(row[1])

    label_name = model.get_outputs()[0].name
    probs = model.run([label_name], {input.name: image})[0]

    result = list(zip(tags, probs[0]))

    # rating = max(result[:general_index], key=lambda x: x[1])
    general = [item for item in result[general_index:character_index] if item[1] > threshold]
    character = [item for item in result[character_index:] if item[1] > character_threshold]

    all = character + general
    remove = [s.strip() for s in exclude_tags.lower().split(",")]
    all = [tag for tag in all if tag[0] not in remove]

    res = ("" if trailing_comma else ", ").join((item[0].replace("(", "\\(").replace(")", "\\)") + (", " if trailing_comma else "") for item in all))

    print(res)
    return res

def download_model(model, client_id, node):
    hf_endpoint = os.getenv("HF_ENDPOINT", defaults["HF_ENDPOINT"])
    if not hf_endpoint.startswith("https://"):
        hf_endpoint = f"https://{hf_endpoint}"
    if hf_endpoint.endswith("/"):
        hf_endpoint = hf_endpoint.rstrip("/")

    url = config_autotagger["models"][model]
    url = url.replace("{HF_ENDPOINT}", hf_endpoint)
    url = f"{url}/resolve/main/"
    try:
        download_to_file(f"{url}model.onnx", os.path.join(models_dir,f"{model}.onnx"))
        download_to_file(f"{url}selected_tags.csv", os.path.join(models_dir,f"{model}.csv"))
    except Exception as err:
        log("Unable to download model. Download files manually or try using a HF mirror/proxy website by setting the environment variable HF_ENDPOINT=https://.....", "ERROR", True)
        raise
    update_node_status(client_id, node, None)
    return web.Response(status=200)

@PromptServer.instance.routes.get("/levelpixeladvanced/autotagger/tag")
async def get_tags(request):
    if "filename" not in request.rel_url.query:
        return web.Response(status=404)

    type = request.query.get("type", "output")
    if type not in ["output", "input", "temp"]:
        return web.Response(status=400)

    target_dir = get_comfy_dir(type)
    image_path = os.path.abspath(os.path.join(
        target_dir, request.query.get("subfolder", ""), request.query["filename"]))
    c = os.path.commonpath((image_path, target_dir))
    if os.path.commonpath((image_path, target_dir)) != target_dir:
        return web.Response(status=403)

    if not os.path.isfile(image_path):
        return web.Response(status=404)

    image = Image.open(image_path)

    models = get_installed_models()
    default = defaults["model"] + ".onnx"
    model = default if default in models else models[0]

    return web.json_response(await tag(image, model, client_id=request.rel_url.query.get("clientId", ""), node=request.rel_url.query.get("node", "")))

class Autotagger:
    @classmethod
    def INPUT_TYPES(s):
        extra = [name for name, _ in (os.path.splitext(m) for m in get_installed_models()) if name not in known_models]
        models = known_models + extra
        return {"required": {
            "image": ("IMAGE", ),
            "model": (models, { "default": defaults["model"] }),
            "threshold": ("FLOAT", {"default": defaults["threshold"], "min": 0.0, "max": 1, "step": 0.05}),
            "character_threshold": ("FLOAT", {"default": defaults["character_threshold"], "min": 0.0, "max": 1, "step": 0.05}),
            "replace_underscore": ("BOOLEAN", {"default": defaults["replace_underscore"]}),
            "trailing_comma": ("BOOLEAN", {"default": defaults["trailing_comma"]}),
            "exclude_tags": ("STRING", {"default": defaults["exclude_tags"]}),
        }}

    RETURN_TYPES = ("STRING",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "tag"
    OUTPUT_NODE = False

    CATEGORY = "LevelPixel/VLM"

    def tag(self, image, model, threshold, character_threshold, exclude_tags="", replace_underscore=False, trailing_comma=False):
        tensor = image*255
        tensor = np.array(tensor, dtype=np.uint8)
        tags = []
        for i in range(tensor.shape[0]):
            img = Image.fromarray(tensor[i])
            tags.append(tag(img, model, threshold, character_threshold, exclude_tags, replace_underscore, trailing_comma))
        return {"ui": {"tags": tags}, "result": (tags,)}

NODE_CLASS_MAPPINGS = {
    "Autotagger|LP": Autotagger,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Autotagger|LP": "Autotagger [LP]",
}
