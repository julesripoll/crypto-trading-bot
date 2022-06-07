"""main program. on va pouvoir l'appeller en ligne de commande avec plusieurs modes genre train, test local, run online etc"""
from time import time
import functions, params
import matplotlib.pyplot as plt
from tf_agents.metrics import tf_metrics
from tf_agents.drivers.dynamic_episode_driver import DynamicEpisodeDriver
import argparse
from tf_agents.policies import PolicySaver
import tensorflow as tf

parser = argparse.ArgumentParser()
parser.add_argument('--mode', type=str, default = 'train', help='execution mode')
args = parser.parse_args()
mode = args.mode

if mode=='train':

    train_env=params.train_env
    agent=params.agent
    losses=functions.train(environment=train_env,agent=agent,train_ite=10)
    policy=PolicySaver(policy=agent.policy)
    policy.save('/Users/julesripoll/Developer/Trading bots/Trading bot crypto/policy')
    plt.plot(losses)
    plt.savefig('loss.png')
    plt.show()

if mode=='eval':
    
    eval_env=params.eval_env
    trained_policy=tf.compat.v2.saved_model.load('/Users/julesripoll/Developer/Trading bots/Trading bot crypto/policy')
    avg_return=tf_metrics.AverageReturnMetric()
    observer=[avg_return]
    eval_driver=DynamicEpisodeDriver(env=eval_env,policy=trained_policy,observers=observer,num_episodes=10)
    _=eval_driver.run()




