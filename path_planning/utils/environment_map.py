import numpy as np
from PIL import Image, ImageOps




def load_heightmap(filepath, show = False):
    #load in a greyscale image as a heightmap of an environment
    #return a 2D numpy array with height values 
    # (x,y)
    # (0,0) ----> x+
    # 
    # |
    # |
    # |
    # v
    #
    # y+

    #load image
    image = Image.open(filepath).convert('L')

    # convert image to numpy array w/ brightness values between 0 and 255
    data = np.asarray(image)

    if show:
        print(data.shape)
        plt.imshow(data, cmap = 'gray')
        plt.show()
    return data





