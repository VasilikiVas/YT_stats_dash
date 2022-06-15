"""
Author: Maris Koopmans
Project: YouTube statistics visualization

License for 3rd party use: Anyone can use this lol I don't mind
"""

from transformers import ViTForImageClassification, ViTFeatureExtractor
from tqdm import tqdm
from PIL import Image
import torch
import json
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


def load_model(device):
    """
    Loads in a pre-trained ViT model for latent image representation

    args:
        - device: what device the model should be on
    returns:
        - model: pre-trained ViT model
        - feature_extractor: pre-trained feature extractor for processing images
    """
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
    # Get the latent representation by passing it through the network
    latent_vecs = model(pixel_values)

    return latent_vecs


def generate_statistics(out_file):
    """
    Function to generate all thumbnail statistics.

    args:
        - out_file: path to the file where the thumbnail statistics should be saved (JSON)
    """

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}\n")

    # Define thumbnail path
    thumbnail_path = "../data/thumbnails/"

    with open("../data/videos_info.json") as f:
        print("Loading creator data")
        creator_info = json.load(f)
    print("Finished loading creator data\n")

    model, feature_extractor = load_model(device)
    creators_stats = {}

    print("Calculating thumbnail statistics for all creators\n")
    for creator in tqdm(list(creator_info.keys())):
        stats_dic = {}
        all_thumbnails = [Image.open(thumbnail_path + vid_dict['id'] + "_high.jpg") 
                            for vid_dict in creator_info[creator]]

        latents = get_latent_vectors(model, feature_extractor, all_thumbnails, device)

        # Save the relevant statistics
        # stats_dic['all_latents'] = latents.detach().numpy().tolist()
        stats_dic['mean_latent'] = torch.mean(latents, dim=0).detach().numpy().tolist()
        stats_dic['stdev'] = torch.sum(torch.std(latents, dim=0)).detach().numpy().tolist()

        creators_stats[creator] = stats_dic

    print("Finished calculating statistics\n")
    print(f"Writing thumbnail statistics to file {out_file}")

    with open(out_file, 'w') as f:
        json.dump(creators_stats, f)


if __name__ == '__main__':
    out_file = "../data/thumbnail_stats.json"
    generate_statistics(out_file)