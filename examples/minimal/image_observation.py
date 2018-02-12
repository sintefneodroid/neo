import neodroid.wrappers.gym_wrapper as neogym
from PIL import Image
import matplotlib.pyplot as plt

env = neogym.make('camera_observation', connect_to_running=False)

while True:
  obs, rew, term, info = env.step(0)
  #im = info.observer('ColorCamera')
  im = env.sensor('ColorCamera').observation_value
  #im.seek(0)
  #im = Image.open(im)
  #plt.imshow(im)
  #plt.show()