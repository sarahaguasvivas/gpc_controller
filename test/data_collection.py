from gym.block_gym import *
import time
from datetime import date

B = BlockGym()

B.reset()

actions1 = list(np.arange(130, -150, -0.3))
actions2 = list(np.arange(130, -150, -0.3))

today = date.today()
f = open("data_" + today.strftime("%b_%d_%Y_7")+".txt", "w+")

try:
    for i in actions1:
        for j in actions2:
            B.step(action=[i, j])
            #time.sleep(0.5)
            print i, j
            data = B.get_observation() + B.get_real_position()
            data = data + [i, j]
            print >> f, data

    B.reset()
except:
    f.close()
    B.reset()
