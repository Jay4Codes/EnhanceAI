from glob import glob  #
# Importing required dependencies from MIRNet
from mirnet.inference import Inferer
from mirnet.utils import plot_result
import time

start = time.time()
inferer = Inferer()


# inferer.download_weights('1sUlRD5MTRKKGxtqyYDpTv7T3jOW6aVAL')

inferer.build_model(num_rrg=3, num_mrb=2, channels=64, weights_path=r'C:\Users\ariha\Desktop\Hackathons & Projects\LOC-Image-Editor\low-light-image-enhancing\MIRNet\low_light_weights_best.h5')
inferer.model.save('mirnet-saved-model')

img_test = r"C:\Users\ariha\Desktop\Hackathons & Projects\LOC-Image-Editor-bad-git\MIRNet low light dataset\eval15\low\1.png"
true_image = r"C:\Users\ariha\Desktop\Hackathons & Projects\LOC-Image-Editor-bad-git\MIRNet low light dataset\eval15\high\1.png"

original_image, output_image = inferer.infer(img_test)
print(time.time() - start)
plot_result(original_image, output_image)