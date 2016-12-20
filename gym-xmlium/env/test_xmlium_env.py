#!/usr/bin/python
import gym
import numpy as np

env = gym.make('xmlium-v0')
env.configure(remotes=1)


while 1:
	observation = env.reset()
	done = False
	obser, r, done, info = env.step()
	env.render()
	time.sleep(0.3)
