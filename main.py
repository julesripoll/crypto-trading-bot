"""main program. on va pouvoir l'appeller en ligne de commande avec plusieurs modes genre train, test local, run online etc"""
import functions, params
import matplotlib.pyplot as plt
from tf_agents.metrics import tf_metrics
from tf_agents.drivers.dynamic_episode_driver import DynamicEpisodeDriver

train_env=params.train_env
agent=params.agent

losses=functions.train(environment=train_env,agent=agent,train_ite=2)

avg_return=tf_metrics.AverageReturnMetric()
observer=[avg_return]
eval_env=params.eval_env
time_step = eval_env.reset()
print(time_step)
driver=DynamicEpisodeDriver(env=eval_env,policy=agent.policy,observers=observer,num_episodes=10)
time_step, _ = driver.run(time_step)


plt.plot(losses)
plt.savefig('loss.png')
plt.show()


