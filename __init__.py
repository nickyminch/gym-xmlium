from gym.envs.registration import register

register(
    id='xmlium-v0',
    entry_point='gym_xmlium.envs:XmliumEnv',
    timestep_limit=500,
)
