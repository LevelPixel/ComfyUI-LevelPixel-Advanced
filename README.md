## Level Pixel nodes for ComfyUI - Advanced nodes

![banner_LevelPixel_with_logo](https://github.com/user-attachments/assets/ef79f2c9-04fb-485f-aba5-6cd00cb14d8c)

The purpose of this package is to collect the most necessary and atomic nodes for working with LLM and VLM models with GGUF format. Installation and maintenance of LLM and VLM nodes based on LLaVA is more complex, so this node package should now be installed separately from the main Level Pixel node package.

**In this Level Pixel Advanced node pack you will find:**
LLM nodes, LLaVa and other VLM nodes, Autotagger, RAM autotagger, WD Autotagger

Recommend that you install the main node package from Level Pixel:

[https://github.com/LevelPixel/ComfyUI-LevelPixel](https://github.com/LevelPixel/ComfyUI-LevelPixel)

The official repository of the current node package is located at this link:

[https://github.com/LevelPixel/ComfyUI-LevelPixel-Advanced](https://github.com/LevelPixel/ComfyUI-LevelPixel-Advanced)

## Contacts:

For cooperation, suggestions and ideas you can write to email:
levelpixel.dev@gmail.com

# Installation:

### Pre-Installation:

Before running ComfyUI with this node package, you should make sure that you have the following programs and libraries installed so that ComfyUI can compile the necessary libraries and programs for llama-cpp-python (the main library that allows you to use any current GGUF models and neural network architectures):

1) `CUDA drivers` - install the latest version.
  Download: [https://developer.nvidia.com/cuda-downloads](https://developer.nvidia.com/cuda-downloads)
2) `Visual Studio 2022 Community IDE` with libraries for compiling C++ programs, specifically with individual components (select them in Visual Studio Installer when installing/modifying Visual Studio 2022):

* MSVC v143 - VS 2022 C++ x64/x86 build tools (Latest)
* MSVC v143 - VS 2022 C++ x64/x86 build tools (v14.38-17.8)
* C++ Cmake tools for Windows
* C++ Cmake tools for Linux and Mac  

  Download: [https://visualstudio.microsoft.com/downloads](https://visualstudio.microsoft.com/downloads)

3) `CMAKE official distribution` - download and install the latest version.
  Download: [https://cmake.org/download](https://cmake.org/download)

4) `llama-mtmd-cli` - if you want to use Qwen2.5-VL gguf, you need to download the Llama.cpp (llama-mtmd-cli) libraries from this link:
  Download: [https://github.com/ggml-org/llama.cpp/releases](https://github.com/ggml-org/llama.cpp/releases)
  Choose the archive that suits your system. Probably, for you it will be `llama-b5317-bin-win--cu12.4-x64.zip`
  After downloading, go to the path:
  `ComfyUI\custom_nodes\ComfyUI-LevelPixel-Advanced\nodes\vlm\llama-mtmd-cli`
  And unzip the downloaded archive here.
  The llama-mtmd-cli folder should contain the llama-mtmd-cli.exe file and other libraries from the archive:
  `ComfyUI\custom_nodes\ComfyUI-LevelPixel-Advanced\nodes\vlm\llama-mtmd-cli\llama-mtmd-cli.exe`

### Installation package using ComfyUI Manager (recommended):

Install [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager) and do steps introduced there to install this repo 'ComfyUI-LevelPixel-Advanced'.
The nodes of the current package will be updated automatically when you click "Update ALL" in ComfyUI Manager.

### Alternative installation package:

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

  `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.9\libnvvp`
  `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.9\bin`
* In System environment variables, add the `CMAKE_ARGS` variable and set it to the following:
  `-DGGML_CUDA=on -DCMAKE_GENERATOR_TOOLSET='cuda=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.9'`

Save the changes made to System environment variables.
Reboot the system.

If the node package still does not install at startup, try to forcefully remove the remains of the llama-cpp-python package for your python.
For example, you can run the following command in the `python_embeded` folder (if you are using the portable version of ComfyUI):

`python.exe -m pip uninstall llama-cpp-python`

After that, run ComfyUI again.

If you still get errors, restart your PC, this may help (sometimes during installation the cache gets damaged and remains in the computer's RAM).

If these tips don't help - study the logs and the cause of the error, read docs about building llama.cpp ([https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md)), and then talk to some powerful neural network about this error - it will probably help you solve your problem.

# Features

All nodes Level Pixel:

<img width="1171" alt="level-pixel-nodes_2" src="https://github.com/user-attachments/assets/792e43d8-fd96-4a27-bf4b-db84261b6014">

## Multimodal Generator node

Multimodal Generator Advanced - New node on new technology of multimodal neural models based on GGUF. Supports Qwen2.5-VL of GGUF format.
Experimental node! It is not recommended to use it in fully autonomous workflows yet.

How to use Multimodal Generator node:

1. **Download the Qwen 2.5 VL gguf file**:  
   [https://huggingface.co/Mungert/Qwen2.5-VL-7B-Instruct-GGUF/tree/main](https://huggingface.co/Mungert/Qwen2.5-VL-7B-Instruct-GGUF/tree/main)  
   Choose a gguf file **without** the mmproj in the name  
   Example gguf file:  
   [https://huggingface.co/Mungert/Qwen2.5-VL-7B-Instruct-GGUF/resolve/main/Qwen2.5-VL-7B-Instruct-q8_0.gguf](https://huggingface.co/Mungert/Qwen2.5-VL-7B-Instruct-GGUF/resolve/main/Qwen2.5-VL-7B-Instruct-q8_0.gguf)  
   Copy this file to ComfyUI/models/LLavacheckpoints.
2. **Download the Qwen 2.5 VL mmproj file (this is clip model):**  
   [https://huggingface.co/Mungert/Qwen2.5-VL-7B-Instruct-GGUF/tree/main](https://huggingface.co/Mungert/Qwen2.5-VL-7B-Instruct-GGUF/tree/main)  
   Choose a file **with** mmproj in the name  
   Example mmproj file:  
   [https://huggingface.co/Mungert/Qwen2.5-VL-7B-Instruct-GGUF/resolve/main/Qwen2.5-VL-7B-Instruct-mmproj-bf16.gguf](https://huggingface.co/Mungert/Qwen2.5-VL-7B-Instruct-GGUF/resolve/main/Qwen2.5-VL-7B-Instruct-mmproj-bf16.gguf)  
   Copy this file to ComfyUI/models/LLavacheckpoints.  

3. **Run ComfyUI and add to workflow node Multimodal Generator Advanced [LP]. Choose ckpt model and clip, pin image and write prompt.**

## LLaVa nodes

A node that generates text using the LLM model and CLIP by image and prompt with subsequent unloading of the model from memory.

Our LLava nodes support the latest LLM and VLM models, and should support future ones (please let us know if any models stop working).

The core functionality is taken from [ComfyUI_VLM_nodes](https://github.com/gokayfem/ComfyUI_VLM_nodes) and belongs to its authors.

Mainly supports only Mistral (with clip for images) and Llama (with clip for images) models. 

At the moment the nodes are obsolete (but still in support status), instead of them it is supposed to develop "Multimodal Generator nodes" based on llama-mtmd for using Qwen2.5-VL, Bagel and other multimodal neural networks.

## LLM nodes

A node that generates text using the LLM model with subsequent unloading of the model from memory. Useful in those workflows where there is constant switching between different models and technologies under conditions of insufficient RAM of the video processor.

Our LLM nodes support the latest LLM and CLIP models, and should support future ones (please let us know if any models stop working).

The core functionality is taken from [ComfyUI_VLM_nodes](https://github.com/gokayfem/ComfyUI_VLM_nodes) and belongs to its authors.

## Autotagger nodes based on WD tagger models

An image autotagger that creates highly relevant tags using fast and ultra-accurate, highly specialized models. More diverse models are planned to be added to the list of models in the future.

This node allows it to be used in cycles and conditions (in places where it is not necessary to execute this node according to the specified conditions), since it is not a node with mandatory execution.

The core functionality is taken from [ComfyUI-WD14-Tagger](https://github.com/pythongosssss/ComfyUI-WD14-Tagger) and belongs to its authors.

## Image Remove Background

A more improved version of nodes for removing background for ComfyUI with an extended list of models.

There are three separate nodes that implement different functionality for different neural models:
* `Image Remove Background (RMBG)` - RECOMMENDED! The most powerful node to use, which uses the most powerful model RMBG-2.0 for background removal. 
* `Image Remove Background (BiRefNet)` - Recommended for super-fast background removal with high quality. Uses the latest generation BiRefNet models that perfectly remove any background in a fraction of a second on the GPU.
* `Image Remove Background (rembg)` - Not recommended for normal use and requires additional settings (read below). It differs in that it allows you to include other special types of neural networks to remove the background in certain situations, but the models will not always be the latest generation for this node.

To use on GPU, at least CUDA 12.4 (Pytorch cu124) is required, so I recommend upgrading to newer versions of ComfyUI and Pytorch.

To use `Image Remove Background (rembg)` effectively on your GPU, you should make sure that you do not have onnxruntime installed together with onnxruntime-gpu. When you run ComfyUI, my package will tell you in the console that you have a conflict between onnxruntime and onnxruntime-gpu.

Solution:
Remove onnxruntime, leaving only pure onnxruntime-gpu.
To do this, do the following:
Close ComfyUI and run the script at `.\ComfyUI\custom_nodes\ComfyUI-LevelPixel-Advanced\scripts\remove_onnxruntime.bat`

The core functionality is taken from [RemBG nodes for ComfyUI](https://github.com/Loewen-Hob/rembg-comfyui-node-better) and from [ComfyUI-RMBG](https://github.com/1038lab/ComfyUI-RMBG) and belongs to its authors.

## Recognize Anything Model (RAM++)

The counterpart to Segment Anything Model (SAM)

This is an image recognition node for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) based on the RAM++ model from [xinyu1205](https://huggingface.co/xinyu1205).

* [https://huggingface.co/xinyu1205/recognize-anything-plus-model](https://huggingface.co/xinyu1205/recognize-anything-plus-model)
* [https://github.com/xinyu1205/recognize-anything](https://github.com/xinyu1205/recognize-anything)
* This node outputs a string of tags with all the recognized objects and elements in the image
* 3 different models.
* RAM and RAM++ outputs tags in English and Chinese language

Furthermore you need to download the [RAM](https://huggingface.co/xinyu1205/recognize_anything_model/resolve/main/ram_swin_large_14m.pth), [RAM++](https://huggingface.co/xinyu1205/recognize-anything-plus-model/resolve/main/ram_plus_swin_large_14m.pth) and [tag2text](https://huggingface.co/xinyu1205/recognize_anything_model/resolve/main/tag2text_swin_14m.pth) models and place it in the /ComfyUI/models/rams/ folder or use the [ComfyUI-Manager](https://github.com/Comfy-Org/ComfyUI-Manager) model downloader.

You can also configure the location in 'extra\_model\_paths.yaml' in the Confyui folder.

# Credits

ComfyUI/[ComfyUI](https://github.com/comfyanonymous/ComfyUI) - A powerful and modular stable diffusion GUI.

VLM nodes for ComfyUI/[ComfyUI_VLM_nodes](https://github.com/gokayfem/ComfyUI_VLM_nodes) - Best VLM nodes for ComfyUI.

WD autotagger node for ComfyUI/[ComfyUI-WD14-Tagger](https://github.com/pythongosssss/ComfyUI-WD14-Tagger) - Source ComfyUI nodes for WD autotagger

RAM node for ComfyUI/[ComfyUI-Hangover-Recognize_Anything](https://github.com/Hangover3832/ComfyUI-Hangover-Recognize_Anything) - Source ComfyUI nodes for RAM (source repository is archived, but we will continue to support RAM nodes)

RAM node for ComfyUI/[ComfyUI-Hangover-Recognize_Anything](https://github.com/Hangover3832/ComfyUI-Hangover-Recognize_Anything) - Source ComfyUI nodes for RAM (source repository is archived, but we will continue to support RAM nodes)

RemBG nodes for ComfyUI/[rembg-comfyui-node](https://github.com/Loewen-Hob/rembg-comfyui-node-better) - RemBG nodes for ComfyUI.

RemBG software package/[rembg](https://github.com/danielgatis/rembg) - Software to remove background for any object in the picture.

RMBG nodes for ComfyUI/[ComfyUI-RMBG](https://github.com/1038lab/ComfyUI-RMBG) - Thanks for the awesome code and implementation of using BiRefNet and RMBG-2.0 models in very convenient and customizable nodes. Note - when using Image Remove Background (RMBG) and Image Remove Background (BiRefNet) you agree to the GPL-3.0 License as stated by the original author of the functionality. The rest of the ComfyUI-LevelPixel-Advanced package uses the Apache-2 License, as the rest of the package does not use Image Remove Background (RMBG) and Image Remove Background (BiRefNet) directly.

# License

Copyright (c) 2024-present [Level Pixel](https://github.com/LevelPixel)

Licensed under Apache-2.0 License
