import os
import torch
import rlcard
from rlcard.agents.dqn_agent_pytorch import DQNAgent
from rlcard.agents import RandomAgent
from rlcard.utils import set_global_seed, tournament
from rlcard.utils import Logger

# Make environment
env = rlcard.make('doudizhu', config={'seed': 0})
eval_env = rlcard.make('doudizhu', config={'seed': 0})

# Set the iterations numbers and how frequently we evaluate/save plot
evaluate_every = 100
evaluate_num = 10000
episode_num = 100000

# The intial memory size
memory_init_size = 1000

# Train the agent every X steps
train_every = 1

# The paths for saving the logs and learning curves
log_dir = './experiments/doudizhu_dqn_result/'

# Set a global seed
set_global_seed(0)

# Set up the agents
agent = DQNAgent(
                scope='dqn',
                action_num=env.action_num,
                replay_memory_init_size=memory_init_size,
                train_every=train_every,
                state_shape=env.state_shape,
                mlp_layers=[512,512])
random_agent = RandomAgent(action_num=eval_env.action_num)

env.set_agents([agent, random_agent, random_agent])
eval_env.set_agents([agent, random_agent, random_agent])


# Init a Logger to plot the learning curve
logger = Logger(log_dir)

for episode in range(episode_num):

    # Generate data from the environment
    trajectories, _ = env.run(is_training=True)

    # Feed transitions into agent memory, and train the agent
    for ts in trajectories[0]:
        agent.feed(ts)

    # Evaluate the performance. Play with random agents.
    if episode % evaluate_every == 0:
        logger.log_performance(env.timestep, tournament(eval_env, evaluate_num)[0])

# Close files in the logger
logger.close_files()

# Plot the learning curve
logger.plot('DQN')

# Save model
save_dir = 'models/doudizhu_dqn'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)


