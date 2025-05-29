import numpy as np
import torch
from PIL import Image

model_list = [
'birefnet-general', # BEST! Recommended! A pre-trained model for general use cases. Source - https://github.com/ZhengPeng7/BiRefNet
'birefnet-massive', # A pre-trained model with massive dataset Source - https://github.com/ZhengPeng7/BiRefNet
'birefnet-general-lite', # A light pre-trained model for general use cases. Source - https://github.com/ZhengPeng7/BiRefNet
'birefnet-portrait', # A pre-trained model for human portraits. Source - https://github.com/ZhengPeng7/BiRefNet
'birefnet-dis', # A pre-trained model for dichotomous image segmentation (DIS). Source - https://github.com/ZhengPeng7/BiRefNet
'birefnet-hrsod', # A pre-trained model for high-resolution salient object detection (HRSOD). Source - https://github.com/ZhengPeng7/BiRefNet
'birefnet-cod', # A pre-trained model for concealed object detection (COD). Source - https://github.com/ZhengPeng7/BiRefNet
'u2net', # A pre-trained model for general use cases. Source - https://github.com/xuebinqin/U-2-Net
'u2netp', # A lightweight version of u2net model. Source - https://github.com/xuebinqin/U-2-Net
'u2net_human_seg', # A pre-trained model for human segmentation. Source - https://github.com/xuebinqin/U-2-Net
'u2net_cloth_seg', # A pre-trained model for Cloths Parsing from human portrait. Here clothes are parsed into 3 category: Upper body, Lower body and Full body. Source - https://github.com/levindabhi/cloth-segmentation
'silueta', # Same as u2net but the size is reduced to 43Mb. Source - https://github.com/xuebinqin/U-2-Net/issues/295
'isnet-general-use', # A new pre-trained model for general use cases. Source - https://github.com/xuebinqin/DIS
'isnet-anime', # A high-accuracy segmentation for anime character. Source - https://github.com/SkyTNT/anime-segmentation
'sam' # A pre-trained model for any use cases. Source - https://github.com/danielgatis/rembg/releases/download/v0.0.0/vit_b-decoder-quant.onnx
]

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)
        
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def list_model():
    return model_list

class ImageRemoveBackground:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name": (list_model(), ),
                "image": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "remove_background"
    CATEGORY = "LevelPixel/Image"

    def remove_background(self, image, model_name):
        from rembg import new_session, remove
        session = new_session(model_name)
        image = pil2tensor(remove(tensor2pil(image), session = session))
        return (image,)
  
NODE_CLASS_MAPPINGS = {
    "ImageRemoveBackground|LP": ImageRemoveBackground
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageRemoveBackground|LP": "Image Remove Background (rembg) [LP]",
}
