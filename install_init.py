import os
import json
import shutil
import platform
import subprocess
import sys
import importlib.util
import re
import inspect
from requests import get
from server import PromptServer
import subprocess
import sys
from importlib import metadata

package_name_llama_cpp_python = "llama-cpp-python"
min_version_llama_cpp_python = "0.3.14"
version_llama_cpp_python =   f"{package_name_llama_cpp_python}>={min_version_llama_cpp_python}"

def verify_python_support():
    version = tuple(map(int, platform.python_version_tuple()[:2]))
    if version < (3, 8):
        print("Warning: Python 3.8 or higher is required")
        return False
    return True

def verify_pypy_support(system_info):
    if 'pp' in system_info['python_version']:
        pp_ver = system_info['python_version'][2:4]
        if pp_ver not in ['38', '39', '310']:
            print("Warning: Current PyPy version may not be supported")
            return False
        if system_info['platform_tag'] not in ['linux_i686', 'linux_x86_64', 'win_amd64', 
                                             'macosx_10_15_x86_64', 'macosx_10_9_x86_64']:
            print("Warning: Current platform may not be supported for PyPy")
            return False
    return True

def get_python_version():
    version_match = re.match(r"3\.(\d+)", platform.python_version())
    if version_match:
        return "3" + version_match.group(1)
    else:
        return None

def get_system_info():
    system_info = {
        'gpu': False,
        'cuda_version': None,
        'rocm_version': None,
        'python_version': get_python_version(),
        'os': platform.system().lower(),
        'arch': platform.machine().lower(),
        'platform_tag': None
    }

    # Determine platform-specific tags
    if system_info['os'] == 'linux':
        if system_info['arch'] == 'x86_64':
            system_info['platform_tag'] = 'linux_x86_64'
        elif system_info['arch'] == 'i686':
            system_info['platform_tag'] = 'linux_i686'
        elif system_info['arch'] == 'aarch64':
            system_info['platform_tag'] = 'linux_aarch64'
    elif system_info['os'] == 'windows':
        if system_info['arch'] == 'amd64':
            system_info['platform_tag'] = 'win_amd64'
        elif system_info['arch'] == 'x86':
            system_info['platform_tag'] = 'win32'
    elif system_info['os'] == 'darwin':
        if system_info['arch'] == 'x86_64':
            # Intel Mac
            if 'pp' in system_info['python_version']:
                system_info['platform_tag'] = 'macosx_10_15_x86_64'
            else:
                py_ver = int(system_info['python_version'][3:])
                if py_ver >= 12:
                    system_info['platform_tag'] = 'macosx_10_13_x86_64'
                else:
                    system_info['platform_tag'] = 'macosx_10_9_x86_64'
        elif system_info['arch'] == 'arm64':
            # Apple Silicon (M1/M2/M3)
            print("Apple Silicon detected. llama-cpp-python will be built with Metal support")
            system_info['platform_tag'] = None  # Force source build for optimal Metal support
            system_info['metal'] = True

    # Check for GPU support
    if importlib.util.find_spec('torch'):
        try:
            import torch
            if hasattr(torch.version, 'hip') and torch.version.hip is not None:
                system_info['gpu'] = True
                system_info['rocm_version'] = f"rocm{torch.version.hip}"
            elif torch.cuda.is_available():
                system_info['gpu'] = True
                system_info['cuda_version'] = "cu" + torch.version.cuda.replace(".", "").strip()
        except:
            pass

    return system_info

def latest_lamacpp():
    try:        
        response = get("https://api.github.com/repos/abetlen/llama-cpp-python/releases/latest")
        return response.json()["tag_name"].replace("v", "")
    except Exception:
        return "0.2.20"

def install_package(package_name, extra_args=None):
    command = [sys.executable, "-m", "pip", "install", package_name, "--no-cache-dir"]
    if extra_args:
        command.extend(extra_args.split())
    print("WARNING: Building the llama-cpp-python wheels can take UP TO AN HOUR due to the specific build conditions. This is not an error, just wait.")
    subprocess.check_call(command)

def package_is_installed(package_name):
    return importlib.util.find_spec(package_name) is not None

def install_llama(system_info):
    if not verify_python_support():
        print("ERROR: Unsupported Python version")
        return False

    if not verify_pypy_support(system_info):
        print("WARNING: Unsupported PyPy configuration")

    imported = is_installed(package_name_llama_cpp_python, min_version_llama_cpp_python) # or package_is_installed("llama_cpp")
    if imported:
        print("llama-cpp installed")
        return True

    # Simple pip install for Linux
    if system_info['os'] == 'linux':
        try:
            print("Installing llama-cpp-python via pip")
            install_package(version_llama_cpp_python)
            return True
        except Exception as e:
            print(f"Installation failed: {e}")
            return False

    # If pre-built wheels fail, try GitHub release wheels
    try:
        version = latest_lamacpp()
        platform_tag = system_info['platform_tag']
        
        if platform_tag:
            python_version = system_info['python_version']
            wheel_name = f"llama_cpp_python-{version}-{python_version}-{python_version}-{platform_tag}.whl"
            wheel_url = f"https://github.com/abetlen/llama-cpp-python/releases/download/v{version}/{wheel_name}"
            
            print(f"Attempting to install from {wheel_url}")
            install_package(wheel_url)
            print(f"Successfully installed llama-cpp-python v{version}")
            return True
    except Exception as e:
        print(f"GitHub wheel installation failed: {e}")
        print("Attempting source build with acceleration...")

    # Build from source with appropriate acceleration
    try:
        if system_info.get('metal', False):
            print("Building llama-cpp-python from source with Metal support")
            os.environ['CMAKE_ARGS'] = "-DGGML_METAL=on"
            install_package(version_llama_cpp_python)
            return True
        elif system_info['gpu']:
            if system_info.get('cuda_version'):
                print("Building llama-cpp-python from source with CUDA support")
                # Add ZLUDA support check
                if os.environ.get('ZLUDA_PATH'):
                    print("ZLUDA detected, building with ZLUDA support")
                    os.environ['CMAKE_ARGS'] = "-DGGML_CUDA=on -DGGML_CUDA_ZLUDA=on"
                else:
                    os.environ['CMAKE_ARGS'] = "-DGGML_CUDA=on"
                install_package(version_llama_cpp_python)
                return True
            elif system_info.get('rocm_version'):
                print("Building llama-cpp-python from source with ROCm support")
                os.environ['CMAKE_ARGS'] = "-DGGML_HIPBLAS=on"
                install_package(version_llama_cpp_python)
                return True
    except Exception as e:
        print(f"Accelerated build failed: {e}")
        print("Falling back to CPU-only version")

    # Final fallback - basic CPU version
    try:
        print("Installing CPU-only version")
        install_package(version_llama_cpp_python)
        return True
    except Exception as e:
        print(f"CPU installation failed: {e}")
        return False

config = None

def is_logging_enabled():
    config = get_extension_config()
    if "logging" not in config:
        return False
    return config["logging"]

def log(message, type=None, always=False, name=None):
    if not always and not is_logging_enabled():
        return

    if type is not None:
        message = f"[{type}] {message}"

    if name is None:
        name = get_extension_config()["name"]

    print(f"(levelpixel-advanced-nodes:{name}) {message}")

def get_ext_dir(subpath=None, mkdir=False):
    dir = os.path.dirname(__file__)
    if subpath is not None:
        dir = os.path.join(dir, subpath)

    dir = os.path.abspath(dir)

    if mkdir and not os.path.exists(dir):
        os.makedirs(dir)
    return dir

def get_extension_config(reload=False):
    global config
    if reload == False and config is not None:
        return config

    config_path = get_ext_dir("levelpixeladvanced.json")
    default_config_path = get_ext_dir("levelpixeladvanced.default.json")
    if not os.path.exists(config_path):
        if os.path.exists(default_config_path):
            shutil.copy(default_config_path, config_path)
            if not os.path.exists(config_path):
                log(f"Failed to create config at {config_path}", type="ERROR", always=True, name="???")
                print(f"Extension path: {get_ext_dir()}")
                return {"name": "Unknown", "version": -1}
    
        else:
            log("Missing levelpixeladvanced.default.json, this extension may not work correctly. Please reinstall the extension.",
                type="ERROR", always=True, name="???")
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

def get_web_ext_dir():
    config = get_extension_config()
    name = config["name"]
    dir = get_comfy_dir("web/extensions/levelpixeladvanced")
    if not os.path.exists(dir):
        os.makedirs(dir)
    dir = os.path.join(dir, name)
    return dir

def get_comfy_dir(subpath=None, mkdir=False):
    dir = os.path.dirname(inspect.getfile(PromptServer))
    if subpath is not None:
        dir = os.path.join(dir, subpath)

    dir = os.path.abspath(dir)

    if mkdir and not os.path.exists(dir):
        os.makedirs(dir)
    return dir

def should_install_js():
    return not hasattr(PromptServer.instance, "supports") or "custom_nodes_from_web" not in PromptServer.instance.supports

def is_installed(pkg_name: str, min_version: str = '') -> bool:
    try:
        ver = metadata.version(pkg_name)
        if min_version:
            return tuple(map(int, ver.split('.'))) >= tuple(map(int, min_version.split('.')))
        return True
    except metadata.PackageNotFoundError:
        return False

def install(pkg_spec: str):
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg_spec])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {pkg_spec}: {e}")
        return

def install_onnxruntime():
    import torch
    gpu = torch.cuda.is_available()
    print(f"Found NVIDIA GPU: {gpu}")
    if gpu:
        if is_installed('onnxruntime'):
            print(f"LP >>> Your python has the 'onnxruntime' library installed, although your computer supports 'onnxruntime-gpu'.")
            print(f"LP >>> Solution: If other node packages do not use the 'onnxruntime' library, then remove the 'onnxruntime' library for your python.")
            print(f"LP >>> Close ComfyUI and run the script at .\\ComfyUI\\custom_nodes\\ComfyUI-LevelPixel-Advanced\\scripts\\remove_onnxruntime.bat")
        elif not is_installed('onnxruntime-gpu'):
            install("onnxruntime-gpu>=1.22")
    else:
        if is_installed('onnxruntime-gpu'):
            print(f"LP >>> Your python has the 'onnxruntime-gpu' library installed, but you don't have a GPU.")
            print(f"LP >>> Solution: If other node packages do not use the 'onnxruntime-gpu' library, then remove the 'onnxruntime-gpu' library for your python.")
            print(f"LP >>> Close ComfyUI and run the script at .\\ComfyUI\\custom_nodes\\ComfyUI-LevelPixel-Advanced\\scripts\\remove_onnxruntime.bat")
        elif not is_installed('onnxruntime'):
            install("onnxruntime>=1.22")

def init(check_imports=None):
    log("Init")

    if check_imports is not None:
        import importlib.util
        for imp in check_imports:
            spec = importlib.util.find_spec(imp)
            if spec is None:
                log(f"{imp} is required, please check requirements are installed.",
                    type="ERROR", always=True)
                return False

    install_js()
    install_onnxruntime()
    return True
