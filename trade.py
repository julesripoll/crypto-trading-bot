from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts
import matplotlib.pyplot as plt
import numpy as np

class TradingEnvTrain(py_environment.PyEnvironment):

    def __init__(self, df, window_size, tc, tol, balance=1000):
        self._action_spec= array_spec.BoundedArraySpec(shape=(), dtype=int, minimum=0, maximum=1)
        self._observation_spec= array_spec.BoundedArraySpec(shape=(window_size,df.shape[1]), dtype=float, minimum=0)
        self._episode_ended=False
        self.initial_balance=balance 
        self.current_balance=balance
        self.train_df=df
        self.train_index=window_size
        self.tc=tc
        self.window_size=window_size
        self.state= df[:][self.train_index-window_size:self.train_index]
        self.position_opened=False
        self.buying_price=0
        self._episode_ended=False
        self.price_history=[]
        self.position_history=[]
        self.total_reward=[]
        self.tolerance=tol

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self.price_history=[]
        self.action_history=[]
        self._episode_ended=False
        self.train_index=self.window_size
        self.current_balance=self.initial_balance
        print(self.train_df[:][self.train_index-self.window_size:self.train_index])
        self.state= self.train_df[:][self.train_index-self.window_size:self.train_index]
        step=ts.restart(observation=self.state)
        #print('reset has been hit',step.step_type)
        self.total_reward=[]
        return step

    def reward(self, ind, buying_price):
        return self.train_df['Close'][ind]-buying_price-self.tc
    
    def _step(self, action):
        if self._episode_ended :
          return self.reset()
        rwd=0
        #print(self.train_index)
        current_price=self.train_df['Close'][self.train_index]
        
        if action==0: #buy
            self._action_spec= array_spec.BoundedArraySpec(shape=(), dtype=int, minimum=1, maximum=2)
            rwd=0
            self.buying_price=current_price
            self.current_balance-=current_price
            self.position_opened=True

        if action==1 and self.position_opened: #hold on bought crypto
            self._action_spec= array_spec.BoundedArraySpec(shape=(), dtype=int, minimum=1, maximum=2)

        elif action==1 and self.position_opened==False: #hold on nothing
            self._action_spec= array_spec.BoundedArraySpec(shape=(), dtype=int, minimum=0, maximum=1)

        else: #sell
            self._action_spec= array_spec.BoundedArraySpec(shape=(), dtype=int, minimum=0, maximum=1)
            self.position_opened=False
            rwd=self.reward(self.train_index,self.buying_price)
            self.current_balance+=current_price
        """
        step retourne 4 valeurs : 
        -observation : une observation de l'environnement, ici une séquence de prix. object
        -reward : une récompense, définie ci dessous, dépendant de l'action effectuée. float
        -done : boolean indiquant si on doit reset l'env, terminant donc l'episode. boolean
        -info : information de notre choix. dict 

        note : les actions possibles dépendent de si on est positionné ou non, et là c'est pas pris en compte.
        """
        self.train_index+=1
        self.state=self.train_df[:][self.train_index-self.window_size:self.train_index]

        if (self.train_index==self.train_df.shape[0]) or self.current_balance<self.initial_balance*self.tolerance:
            self._episode_ended=True
            self.train_index=self.window_size
            step=ts.termination(reward=rwd, observation=self.state)
            #print('episode terminated',step.step_type) #si c'est bien 2 c'est ISLAST
            return step
            """
            ts.termination retourne un TimeStep. si termination à priori ça renvoie un done = true.
            A verifier dans la cellule de validation. 
            Ici la condition d'arrêt c'est d'avoir perdu 40% de l'investissement initial ou d'avoir fini le training set
            """
        else:
            step=ts.transition(reward=rwd, observation=self.state)
            #print('transitioning,',step.step_type) 
            return step 

    def _render(self):
        #dans la pratique très compliqué à implémenter de ce que j'en lis sur internet
        plt.plot(self.total_reward)
        plt.show()

class TradingEnvLive(py_environment.PyEnvironment):
    """TODO"""
    pass