"""main program. on va pouvoir l'appeller en ligne de commande avec plusieurs modes genre train, test local, run online etc"""
import functions, params
import matplotlib.pyplot as plt

train_env=params.train_env
agent=params.agent

losses=functions.train(environment=train_env,agent=agent,train_ite=10)

plt.plot(losses)
plt.savefig('loss1.png')
plt.show()




