from PIL import Image
import torch
import gc
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="timm\\.models")

from ram.models import ram
from ram.models import ram_plus
from ram.models import tag2text
from ram import inference_ram # as inference
from ram import inference_tag2text # as inference
from ram import get_transform
from folder_paths import models_dir, add_model_folder_path, get_folder_paths, get_filename_list, get_full_path
import numpy

rams_dir = f"{models_dir}/rams"

try:
    if rams_dir not in get_folder_paths("rams"):
        raise KeyError
except KeyError:
    add_model_folder_path("rams", rams_dir)

print(f"[Recognize Anything] RAM models found: {', '.join(get_filename_list('rams'))}")


class RecognizeAnything:
    MODEL_NAMES = ["ram_swin_large_14m.pth", "ram_plus_swin_large_14m.pth", "tag2text_swin_14m.pth"] # other/newer models can be added here
    DEVICES = ["cpu", "gpu"] if torch.cuda.is_available() else  ["cpu"]
    IMAGE_SIZES = [384, 448]

    def __init__(self):
        self.model = None
        self.modelname = ""
        self.image_size = 384
        # self.inference = None

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "model": (s.MODEL_NAMES, {"default": s.MODEL_NAMES[1]},),
                "device": (s.DEVICES, {"default": s.DEVICES[0]},),
                "spec_tag2text": ("STRING", {"default": ""},),
                # "tag2text_threshold": ("INT", {"min": 0, "max": 100, "default": 68},),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING",)
    RETURN_NAMES = ("tags", "spec_tags", "caption")
    FUNCTION = "interrogate"
    OUTPUT_NODE = False
    CATEGORY = "LevelPixel/VLM"

    def interrogate(self, image:torch.Tensor, model:str, device:str, spec_tag2text:str):
        dev = torch.device("cuda" if device.lower() == "gpu" else "cpu")
        model_path = get_full_path("rams", model)
        if not model_path:
            raise NameError(f"Model '{model}' not found. Make sure it is in the '/models/rams' folder or add the path in 'extra_model_paths.yaml'")
        self.transform = get_transform(image_size=RecognizeAnything.IMAGE_SIZES[0])

        # delete some tags that may disturb captioning
        # 127: "quarter"; 2961: "back", 3351: "two"; 3265: "three"; 3338: "four"; 3355: "five"; 3359: "one"
        delete_tag_index = [127, 2961, 3351, 3265, 3338, 3355, 3359]

        if (self.model == None) or (self.modelname != model) or (device != self.device):
            del self.model
            gc.collect()
            if (device == "cpu") and torch.cuda.is_available():
                torch.cuda.empty_cache()
            self.model = None
            print(f"[Recognize Anything]: loading model {model_path}, please stand by....")

            if model == RecognizeAnything.MODEL_NAMES[0]:
                self.model = ram(pretrained=model_path, image_size=self.image_size, vit='swin_l')
            elif model == RecognizeAnything.MODEL_NAMES[1]:
                self.model = ram_plus(pretrained=model_path, image_size=self.image_size, vit='swin_l')
            elif model == RecognizeAnything.MODEL_NAMES[2]:
                self.model = tag2text(pretrained=model_path, image_size=self.image_size, vit='swin_b', delete_tag_index=delete_tag_index)
                # self.model.threshold = tag2text_threshold  # threshold for tagging
            else:
                raise ValueError('No valid model was selected', model)

            self.model.eval()
            self.model = self.model.to(dev)

            self.modelname = model
            self.device = device

        tag0 = tag1 = tag2 = ''
        
        for im in image:
            i = 255. * im.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            image = self.transform(img).unsqueeze(0).to(dev)
            if model == RecognizeAnything.MODEL_NAMES[2]:
                res = inference_tag2text(image, self.model, input_tag=spec_tag2text) 
            else:
                res = inference_ram(image, self.model)

            # remove duplicates and reformat the string:
            tag0 =  ", ".join(list(numpy.unique(res[0].split(' | ')))) + '\n'
            tag1 += ", ".join(list(numpy.unique(res[1].split(' | ')))) + '\n' if (len(res) > 1) and res[1] else '\n'
            tag2 += res[2] + '\n' if (len(res) > 2) and res[2] else '\n'
        
        return(tag0, tag1, tag2,)

NODE_CLASS_MAPPINGS = {
    "RecognizeAnything(RAM)|LP": RecognizeAnything,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RecognizeAnything(RAM)|LP": "Recognize Anything (RAM) [LP]",
}