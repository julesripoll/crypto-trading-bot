from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts


class TradingEnvTrain(py_environment.PyEnvironment):

    def __init__(self, df, window_size, tc, balance=1000):
        self._action_spec= array_spec.BoundedArraySpec(shape=(), dtype=int, minimum=0, maximum=2)
        self._observation_spec= array_spec.BoundedArraySpec(shape=(5,df.shape[1]), dtype=float, minimum=0)
        self._episode_ended=False
        self.initial_balance=balance 
        self.current_balance=balance
        self.train_df=df
        self.train_index=window_size
        self.tc=tc
        self.window_size=window_size
        self.state= df[:][self.train_index-window_size:self.train_index]
        self.positioned=False
        self.buying_price=0
        self._episode_ended=False

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self._episode_ended=False
        self.train_index=self.window_size
        self.current_balance=self.initial_balance
        self.state= self.train_df[:][self.train_index-self.window_size:self.train_index]
        step=ts.restart(observation=self.state)
        print('reset has been hit',step.step_type)
        return step

    def reward(self, ind, buying_price):
        return self.train_df['Close'][ind]-buying_price-self.tc
    
    def _step(self, action):
        """
        step retourne 4 valeurs : 
        -observation : une observation de l'environnement, ici une séquence de prix. object
        -reward : une récompense, définie ci dessous, dépendant de l'action effectuée. float
        -done : boolean indiquant si on doit reset l'env, terminant donc l'episode. boolean
        -info : information de notre choix. dict 

        note : les actions possibles dépendent de si on est positionné ou non, et là c'est pas pris en compte.
        """
        if self._episode_ended :
          return self.reset()
        rwd=0
        current_price=self.train_df['Close'][self.train_index]
        if action==0 : #buy
            rwd=0
            self.buying_price=current_price
            self.current_balance-=current_price
            self.positioned=True
        elif action==1: #do nothing
            rwd=0
        elif action==2: #sell
            self.positioned=False
            rwd=self.reward(self.train_index,self.buying_price)
            self.current_balance+=current_price

        self.train_index+=1
        self.state=self.train_df[:][self.train_index-self.window_size:self.train_index]

        if (self.train_index==self.train_df.shape[0]) or self.current_balance<self.initial_balance*0.6:
            self._episode_ended=True
            self.train_index=self.window_size
            step=ts.termination(reward=rwd, observation=self.state)
            print('episode terminated',step.step_type) #si c'est bien 2 c'est ISLAST
            return step
            """
            ts.termination retourne un TimeStep. si termination à priori ça renvoie un done = true.
            A verifier dans la cellule de validation. 
            Ici la condition d'arrêt c'est d'avoir perdu 10% de l'investissement initial ou d'avoir fini le training set
            """
        else:
            step=ts.transition(reward=rwd, observation=self.state)
            print('transitioning,',step.step_type) 
            return step  #s'il ne s'agit pas de la fin d'un épisode. Step type induit par transition

    def _render(self):
        pass



