## Level Pixel nodes for ComfyUI - Advanced nodes

![banner_LevelPixel_with_logo](https://github.com/user-attachments/assets/ef79f2c9-04fb-485f-aba5-6cd00cb14d8c)

The purpose of this package is to collect the most necessary and atomic nodes for working with LLM and VLM models with GGUF format. Installation and maintenance of LLM and VLM nodes based on LLaVA is more complex, so this node package should now be installed separately from the main Level Pixel node package.

**In this Level Pixel Advanced node pack you will find:**
LLM nodes, LLaVa and other VLM nodes

Recommend that you install the main node package from Level Pixel:\
[https://github.com/LevelPixel/ComfyUI-LevelPixel](https://github.com/LevelPixel/ComfyUI-LevelPixel)


The official repository of the current node package is located at this link:\
[https://github.com/LevelPixel/ComfyUI-LevelPixel-Advanced](https://github.com/LevelPixel/ComfyUI-LevelPixel-Advanced)

## Contacts:

For cooperation, suggestions and ideas you can write to email:
levelpixel.dev@gmail.com


# Installation:

### Pre-Installation:

Before running ComfyUI with this node package, you should make sure that you have the following programs and libraries installed so that ComfyUI can compile the necessary libraries and programs for llama-cpp-python (the main library that allows you to use any current gguf models and neural network architectures):

* `CUDA drivers` - install the latest version.\
  Download: [https://developer.nvidia.com/cuda-downloads](https://developer.nvidia.com/cuda-downloads)
* `Visual Studio 2022 Community IDE` with libraries for compiling C++ programs, specifically with individual components (select them in Visual Studio Installer when installing/modifying Visual Studio 2022):
  MSVC v143 - VS 2022 C++ x64/x86 build tools (Latest)\
  MSVC v143 - VS 2022 C++ x64/x86 build tools (v14.38-17.8)\
  C++ Cmake tools for Windows\
  C++ Cmake tools for Linux and Mac\
  Download: [https://visualstudio.microsoft.com/downloads](https://visualstudio.microsoft.com/downloads)
* `CMAKE official distribution` - download and install the latest version.\
  Download: [https://cmake.org/download](https://cmake.org/download)

### Installation Using ComfyUI Manager (recommended):

Install [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager) and do steps introduced there to install this repo 'ComfyUI-LevelPixel-Advanced'.
The nodes of the current package will be updated automatically when you click "Update ALL" in ComfyUI Manager.

### Alternative installation:

Clone the repository:
`git clone https://github.com/LevelPixel/ComfyUI-LevelPixel-Advanced.git`
to your ComfyUI `custom_nodes` directory

The script will then automatically install all custom scripts and nodes.
It will attempt to use symlinks and junctions to prevent having to copy files and keep them up to date.

- For uninstallation:
  - Delete the cloned repo in `custom_nodes`
  - Ensure `web/extensions/levelpixeladvanced` has also been removed
- For manual update:
  - Navigate to the cloned repo e.g. `custom_nodes/ComfyUI-LevelPixel-Advanced`
  - `git pull`

### Troubleshooting:

If you have problems running ComfyUI with this node package, check and do the following:

* The path to Cmake (official distribution, for example, path `C:\Program Files\CMake\bin`) must be at the very top of the Path list in the **System environment variables**. Make sure that the path is at the top of the Path in the **System variables**, and not only in the user variables. If Cmake is not at the top of the list, then some libraries may not compile due to the lack of the current version of the Cmake compiler.
* The path to the current version of your CUDA must be at the very top of the **Path** list in the **System environment variables** (right after Cmake). Make sure that the path is at the top of the Path in the System variables, and not only in the user variables.
  Here are the paths that should be in Path for CUDA (this is an example, substitute your CUDA version for "12.9"):

  `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.9\libnvvp`\
  `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.9\bin`
* In System environment variables, add the `CMAKE_ARGS` variable and set it to the following:\
  `-DGGML_CUDA=on -DCMAKE_GENERATOR_TOOLSET='cuda=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.9'`

Save the changes made to System environment variables.
Reboot the system.

If the node package still does not install at startup, try to forcefully remove the remains of the llama-cpp-python package for your python.
For example, you can run the following command in the `python_embeded` folder (if you are using the portable version of ComfyUI):

`python.exe -m pip uninstall llama-cpp-python`

After that, run ComfyUI again.

If these tips don't help - study the logs and the cause of the error, and then talk to some powerful neural network about this error - it will probably help you solve your problem.

# Features

All nodes Level Pixel:

<img width="1171" alt="level-pixel-nodes_2" src="https://github.com/user-attachments/assets/1a41469d-e29a-474a-8481-da9f3f3e5148">

## LLM nodes

A node that generates text using the LLM model with subsequent unloading of the model from memory. Useful in those workflows where there is constant switching between different models and technologies under conditions of insufficient RAM of the video processor.

Our LLM nodes support the latest LLM and CLIP models, and should support future ones (please let us know if any models stop working).

The core functionality is taken from [ComfyUI_VLM_nodes](https://github.com/gokayfem/ComfyUI_VLM_nodes) and belongs to its authors.

## LLaVa nodes

A node that generates text using the LLM model and CLIP by image and prompt with subsequent unloading of the model from memory.

Our LLava nodes support the latest LLM and VLM models, and should support future ones (please let us know if any models stop working).

The core functionality is taken from [ComfyUI_VLM_nodes](https://github.com/gokayfem/ComfyUI_VLM_nodes) and belongs to its authors.

How to use LLaVa nodes:

1. **Download the Qwen 2.5 VL gguf file**:\
   [https://huggingface.co/Mungert/Qwen2.5-VL-7B-Instruct-GGUF/tree/main
   ](https://huggingface.co/Mungert/Qwen2.5-VL-7B-Instruct-GGUF/tree/main)\
   Choose a gguf file **without** the mmproj in the name\
   Example gguf file:\
   [https://huggingface.co/Mungert/Mungert/Qwen2.5-VL-7B-Instruct-GGUF/resolve/main/Qwen2.5-VL-7B-Instruct-q8_0.gguf
   ](https://huggingface.co/Mungert/Mungert/Qwen2.5-VL-7B-Instruct-GGUF/resolve/main/Qwen2.5-VL-7B-Instruct-q8_0.gguf)\
   Copy this file to ComfyUI/model/Llavacheckpoint.
   
2. **Download the Qwen 2.5 VL mmproj file (this is clip model):**\
   [https://huggingface.co/Mungert/Qwen2.5-VL-7B-Instruct-GGUF/tree/main
   ](https://huggingface.co/Mungert/Qwen2.5-VL-7B-Instruct-GGUF/tree/main)\
   Choose a file **with** mmproj in the name\
   Example mmproj file:\
   [https://huggingface.co/Mungert/Qwen2.5-VL-7B-Instruct-GGUF/resolve/main/Qwen2.5-VL-7B-Instruct-mmproj-bf16.gguf
   ](https://huggingface.co/Mungert/Qwen2.5-VL-7B-Instruct-GGUF/resolve/main/Qwen2.5-VL-7B-Instruct-mmproj-bf16.gguf)\
   Copy this file to ComfyUI/model/Llavacheckpoint.
   
3. **Run ComfyUI and add to workflow node LLava Advanced [LP]. Choose ckpt model and clip, pin image and write prompt.**

# Credits

ComfyUI/[ComfyUI](https://github.com/comfyanonymous/ComfyUI) - A powerful and modular stable diffusion GUI.

VLM nodes for ComfyUI/[ComfyUI_VLM_nodes](https://github.com/gokayfem/ComfyUI_VLM_nodes) - Best VLM nodes for ComfyUI.

# License

Copyright (c) 2024-present [Level Pixel](https://github.com/LevelPixel)

Licensed under Apache License
