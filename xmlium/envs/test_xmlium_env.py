#!/usr/bin/python

import gym
import universe
import time
import numpy as np
#import gym_pull

print(universe.__file__); print(universe.register); print(universe.configuration)

#gym_pull.pull('github.com/nickyminch/gym-xmlium')
#env = gym.make('flashgames.DuskDrive-v0')
env = gym.make('xmlium-v0')
env.configure(remotes='vnc://localhost:5900+15900')
obser = env.reset()

while 1:

	done = False
	obser, r, done, info = env.step()
	env.render()
	time.sleep(0.3)
