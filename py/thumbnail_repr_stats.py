"""
Author: Maris Koopmans
Project: YouTube statistics visualization

License for 3rd party use: Anyone can use this lol I don't mind
"""

from transformers import ViTForImageClassification, ViTFeatureExtractor
from util.constants import Topic
from tqdm import tqdm
from PIL import Image
import torch
import json
import sys
import os

class ImageLatentRepresentationModel(ViTForImageClassification):
    """
    Hook into the ViTForImageClassification Class in order to get the latent
    representations of an image, not just the classification output. Source code
    taken from HuggingFace open-source GitHub:
    https://github.com/huggingface/transformers/blob/main/src/transformers/models/vit/modeling_vit.py
    """

    def __init__(self, config):
        super().__init__(config)

    def forward(self, pixel_values):
        """
        Overwritten forward method to only get latent representation of the image,
        without image classification.

        args:
            - pixel_values: input image, as PyTorch Tensor of shape [1,3,224,224] 
        
        returns:
            - latent_vec: latent vector representing the image
        """
        vit_output = self.vit(pixel_values)
        latent_vec = vit_output[0][:,0,:]

        return latent_vec


def load_model(device, install=True):
    """
    Loads in a pre-trained ViT model for latent image representation

    args:
        - device: what device the model should be on
    returns:
        - model: pre-trained ViT model
        - feature_extractor: pre-trained feature extractor for processing images
    """
    if install:
        print("Installing ViT architecture... This may take a couple of minutes.")
        os.system("pip install -q git+https://github.com/huggingface/transformers.git")
        print("Finished installing.")

    print("Loading pretrained ViT model...")
    model = ImageLatentRepresentationModel.from_pretrained('google/vit-base-patch16-224')
    model.eval()
    model.to(device)
    print("Loaded model")

    feature_extractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224')
    return model, feature_extractor


def get_latent_vectors(model, ft_extr, raw_imgs, device):
    """
    Function to get the latent representation of an image.

    args:
        - model: The pretrained ViT model
        - ft_extr: The feature extractor, used to preprocess the images
        - raw_imgs: The raw thumbnail images
    """
    # Encode the images using the feature extractor
    encodings = ft_extr(images=raw_imgs, return_tensors="pt")
    pixel_values = encodings['pixel_values'].to(device)
    print(f"Size of images in memory: {pixel_values.element_size()*pixel_values.nelement()} bytes")
    # Get the latent representation by passing it through the network
    latent_vecs = model(pixel_values)
    del pixel_values
    return latent_vecs


def generate_repr_stats(out_dir, category: Topic):
    """
    Function to generate all thumbnail latent representation statistics.

    args:
        - out_dir: directory where the statistics should be saved
        - category: the type of content videos
    """

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # device = torch.device('cpu')
    print(f"Using device: {device}\n")

    # Define thumbnail path
    thumbnail_dir = os.path.join("..", "data", "thumbnails")
    
    # Save the thumbnail stats per category
    out_dir = os.path.join(out_dir, "videos")
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    with open(os.path.join("..", "data", f"videos-info_{category.name}.json"), "r") as f:
        print("Loading channel's videos")
        channel_info = json.load(f)
    print("Finished loading channel's videos\n")

    model, feature_extractor = load_model(device, install=False)
    # Print model size
    mem_params = sum([param.nelement()*param.element_size() for param in model.parameters()])
    mem_bufs = sum([buf.nelement()*buf.element_size() for buf in model.buffers()])
    print(f"Memory used by model: {mem_params + mem_bufs} bytes")

    print("Calculating thumbnail latent representation stats for all channels\n")
    for channel in tqdm(list(channel_info.keys())):
        if os.path.isfile(os.path.join(out_dir, channel + "_stats.json")):
            continue
        
        stats_dic = {}

        vid_ids = [vid_dict['id'] for vid_dict in channel_info[channel] if os.path.isfile(os.path.join(thumbnail_dir, vid_dict['id'] + "_high.jpg"))]
        all_thumbnails = [Image.open(os.path.join(thumbnail_dir, vid_dict['id'] + "_high.jpg")) 
                            for vid_dict in channel_info[channel] if os.path.isfile(os.path.join(thumbnail_dir, vid_dict['id'] + "_high.jpg"))]

        print(f'Number of thumbnails: {len(all_thumbnails)}')
        if all_thumbnails:
            latents = get_latent_vectors(model, feature_extractor, all_thumbnails, device)
            latents_save = latents.detach().cpu().numpy().tolist()
        else:
            # If there aren't any thumbnails available save None
            latents = torch.Tensor([])
            latents_save = torch.Tensor([])

        # Save the relevant statistics
        stats_dic['all_latents'] = {vid_ids[i]: latents_save[i] for i in range(len(latents_save))}
        stats_dic['mean_latent'] = torch.mean(latents_save, dim=0).detach().cpu().numpy().tolist()
        stats_dic['stdev'] = torch.sum(torch.std(latents_save, dim=0)).detach().cpu().numpy().tolist()

        with open(os.path.join(out_dir, channel + "_stats.json"), 'w') as f:
            json.dump(stats_dic, f)

        del latents
        torch.cuda.empty_cache()

    print("Finished calculating statistics\n")


if __name__ == '__main__':
    out_dir = os.path.join("..", "data", "thumbnail-latents")
    generate_repr_stats(out_dir, Topic.gaming)