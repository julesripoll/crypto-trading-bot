"""c'est dans ce fichier qu'on définit les fonctions utiles pour main"""
from numpy import random
import numpy as np
from tf_agents.utils import common
from tf_agents.metrics import tf_metrics
from tf_agents.replay_buffers.tf_uniform_replay_buffer import  TFUniformReplayBuffer
from tf_agents.drivers.dynamic_episode_driver import DynamicEpisodeDriver
from tf_agents.policies import random_tf_policy

def first_steps(environment, num_episodes = 5):
  """cette fonction sert à tester un environnement nouvellement créé. Il n'y pas d'agent qui intervienne, les actions sont
  prises randomly."""
  rewards = []
  steps = []

  for i in range(num_episodes):
    time_step = environment.reset()
    episode_reward = 0
    episode_steps = 0
    while not time_step.is_last():
      action=random.randint(0,3)
      time_step = environment.step(action)
      episode_steps += 1
      episode_reward += time_step.reward.numpy()
    print('episode steps', episode_steps)
    print('#########################################################################')
    rewards.append(episode_reward)
    steps.append(episode_steps)

  num_steps = np.sum(steps)
  avg_length = np.mean(steps)
  avg_reward = np.mean(rewards)

  print('num_episodes:', num_episodes, 'num_steps:', num_steps)
  print('avg_length', avg_length, 'avg_reward:', avg_reward)

def compute_avg_return(environment, policy, num_episodes=10):
  """ça vient peut etre du fait que dans le tuto ils demandent un py env et pas tf.
   trouver comment eval les résultats d'un tf env.
   regarder comment le gars de closertoalgotrading fait lui, sur yt"""
  total_return = 0.0
  for _ in range(num_episodes):

    time_step = environment.reset()
    episode_return = 0.0

    while not time_step.is_last():
      action_step = policy.action(time_step)
      time_step = environment.step(action_step.action)
      episode_return += time_step.reward
    total_return += episode_return

  avg_return = total_return / num_episodes
  return avg_return.numpy()[0]

def train(environment,agent,train_ite=100):
    """cette fonction entraine le rnn d'un agent sur un env donné, avec train_ite updates de la loss.
    pour chaque train_ite on fait autant d'episodes que précisé dans le driver.
    note : peut-être passer les buffer etc en paramètres"""
    rdm_policy = random_tf_policy.RandomTFPolicy(action_spec=environment.action_spec(),
                                                time_step_spec=environment.time_step_spec())
    replay_buffer = TFUniformReplayBuffer(
        agent.collect_data_spec,
        batch_size=1,
        max_length=1000
        )
        
    env_steps=tf_metrics.EnvironmentSteps()
    observers=[replay_buffer.add_batch,env_steps]
    driver=DynamicEpisodeDriver(
        environment,
        rdm_policy,
        observers,
        num_episodes=10
    )

    print('est ce que c ça le truc deprecated? oui')
    training_set=replay_buffer.as_dataset(
        sample_batch_size=32,
        num_steps=40
    )
    iterator=iter(training_set)

    # (Optional) Optimize by wrapping some of the code in a graph using TF function. peut etre essayer de virer ça?
    agent.train = common.function(agent.train)

    agent.train_step_counter.assign(0) #compte les train_ite

    # Reset the environment.
    time_step = environment.reset()
    losses=[]

    for _ in range(train_ite):
        # Collect a few steps and save to the replay buffer.
        time_step, _ = driver.run(time_step)
        # Sample a batch of data from the buffer and update the agent's network.
        experience, unused_info = next(iterator)
        train_loss = agent.train(experience).loss
        losses.append(train_loss)
        step = agent.train_step_counter.numpy()
        if step % int(train_ite/10) == 0: #toutes les 10 train_ite on va print la loss
            print('step = {0} : loss = {1}'.format(step, train_loss))

    return losses