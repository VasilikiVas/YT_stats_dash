import numpy as np
import os
from matplotlib import image
from PIL import Image
from tqdm import tqdm
from util.constants import THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT

def crop_black_border_img(img):
    y_nonzero, _, _ = np.nonzero(img)

    # if y_nonzero is empty (all black image) return cropped img
    if not np.any(y_nonzero):
        return img[44:314]    
    
    min_y = y_nonzero.min()
    max_y = y_nonzero.max()

    h, w, _ = img.shape
    if min_y == 0 and max_y == 359:
        # this is a short so we don't want to crop
        # print("short")
        return False
    elif h == THUMBNAIL_HEIGHT and w == THUMBNAIL_WIDTH:
        # only crop the images with the original thumbnail shape 
        # print("cropping")
        return img[44:314]
    elif h == 270 and w == 480:
        # print("image already cropped")
        return img
    else:
        # print("something else")
        return False


def crop_black_border(img_dir, overwrite_img = False):
    """
     Function to crop_black_border of an image
     
     args:
        - img_dir: path to the image directory
        - overwrite_img: flag to set wheather to overwrite the image
    """
    img =image.imread(img_dir)

    y_nonzero, _, _ = np.nonzero(img)

    # if y_nonzero is empty (all black image) return cropped img
    if not np.any(y_nonzero):
        return img[44:314]
    
    min_y = y_nonzero.min()
    max_y = y_nonzero.max()

    h, w, _ = img.shape
    if min_y == 0 and max_y == 359:
        # this is a short so we don't want to crop
        return img
    elif h == THUMBNAIL_HEIGHT and w == THUMBNAIL_WIDTH:
        # only crop the images with the original thumbnail shape 
        img = img[44:314]
        if overwrite_img:
            # overwrite cropped image
            im = Image.fromarray(img)
            im.save(os.path.join(img_dir))
        return img


if __name__ == '__main__':
    thumbnail_dir = os.path.join("..", "data", "thumbnails")
    for img in tqdm(os.listdir(thumbnail_dir)):
        img_dir = os.path.join(thumbnail_dir, img)
        img = crop_black_border(img_dir, overwrite_img = True)
        
        # plt.imshow(img)
        # plt.show()

