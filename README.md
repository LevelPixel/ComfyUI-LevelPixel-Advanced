## Level Pixel nodes for ComfyUI - Advanced nodes

![banner_LevelPixel_with_logo](https://github.com/user-attachments/assets/ef79f2c9-04fb-485f-aba5-6cd00cb14d8c)

The purpose of this package is to collect the most necessary and atomic nodes for working with LLM and VLM models.

**In this Level Pixel Advanced node pack you will find:**
LLM nodes, LLaVa and other VLM nodes

## Contacts:

For cooperation, suggestions and ideas you can write to email:
levelpixel.dev@gmail.com

# Installation:

## Installation Using ComfyUI Manager (recommended):

Install [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager) and do steps introduced there to install this repo 'ComfyUI-LevelPixel-Advanced'.
The nodes of the current package will be updated automatically when you click "Update ALL" in ComfyUI Manager.

## Alternative installation:

Clone the repository:
`git clone https://github.com/LevelPixel/ComfyUI-LevelPixel-Advanced.git`
to your ComfyUI `custom_nodes` directory

The script will then automatically install all custom scripts and nodes.
It will attempt to use symlinks and junctions to prevent having to copy files and keep them up to date.

- For uninstallation:
  - Delete the cloned repo in `custom_nodes`
  - Ensure `web/extensions/levelpixel` has also been removed
- For manual update:
  - Navigate to the cloned repo e.g. `custom_nodes/ComfyUI-LevelPixel`
  - `git pull`

# Features

All nodes Level Pixel:

<img width="1171" alt="level-pixel-nodes_2" src="https://github.com/user-attachments/assets/e3b183b1-23d8-4d8b-bd7f-fae00c6a488c">

## LLM nodes

A node that generates text using the LLM model with subsequent unloading of the model from memory. Useful in those workflows where there is constant switching between different models and technologies under conditions of insufficient RAM of the video processor.

Our LLM nodes support the latest LLM and CLIP models, and should support future ones (please let us know if any models stop working).

The core functionality is taken from [ComfyUI_VLM_nodes](https://github.com/gokayfem/ComfyUI_VLM_nodes) and belongs to its authors.

## LLaVa nodes

A node that generates text using the LLM model and CLIP by image and prompt with subsequent unloading of the model from memory.

Our LLava nodes support the latest LLM models, and should support future ones (please let us know if any models stop working).

The core functionality is taken from [ComfyUI_VLM_nodes](https://github.com/gokayfem/ComfyUI_VLM_nodes) and belongs to its authors.

# Credits

ComfyUI/[ComfyUI](https://github.com/comfyanonymous/ComfyUI) - A powerful and modular stable diffusion GUI.

VLM nodes for ComfyUI/[ComfyUI_VLM_nodes](https://github.com/gokayfem/ComfyUI_VLM_nodes) - Best VLM nodes for ComfyUI.

# License

Copyright (c) 2024-present [Level Pixel](https://github.com/LevelPixel)

Licensed under Apache License
