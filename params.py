"""c'est dans ce fichier qu'on va définir des variables. même ajouter les rp buffer en fait"""
import pandas as pd
import trade
from tf_agents.environments import tf_py_environment
import talib
from tf_agents.networks.q_rnn_network import QRnnNetwork
from tf_agents.agents import DqnAgent
from tf_agents.utils import common
import tensorflow as tf
from tf_agents.replay_buffers.tf_uniform_replay_buffer import  TFUniformReplayBuffer


#print options
pd.set_option('display.max_rows', 6000)
pd.set_option('display.max_columns', 10)

#dataset d'entrainement
eth=pd.read_csv("~/Developer/Trading bots/Trading bot crypto/Data/HitBTC_ETHUSD_1h.csv", sep=",")
eth=eth.drop(['Date', 'Unix Timestamp', 'Symbol','Volume USD'], axis=1)

#ajout d'indicateurs
window_size=5
rsi=pd.DataFrame(talib.RSI(eth['Close'],timeperiod=window_size))
ema=pd.DataFrame(talib.EMA(eth['Close'],timeperiod=window_size))
eth.insert(0,'rsi',rsi)
eth.insert(0,'ema',ema)
eth=eth[5:]
eth.reset_index(inplace=True)

#environnement d'entrainement
train_py_env=trade.TradingEnvTrain(df=eth[:3000], window_size=window_size,tol=0.8,tc=10)
train_env = tf_py_environment.TFPyEnvironment(train_py_env)

eval_py_env=trade.TradingEnvTrain(df=eth[3000:], window_size=window_size,tol=0.8, tc=10)
eval_env=tf_py_environment.TFPyEnvironment(eval_py_env)

#rnn
rnn_net=QRnnNetwork(
    input_tensor_spec=train_env.observation_spec(),
    action_spec=train_env.action_spec(),
    lstm_size=(40,),
    output_fc_layer_params=(20,)
    )

#agent
optimizer = tf.keras.optimizers.Adam(learning_rate=0.1)
global_step=tf.Variable(0)

agent=DqnAgent(
    time_step_spec=train_env.time_step_spec(),
    action_spec=train_env.action_spec(),
    q_network=rnn_net,
    optimizer=optimizer,
    td_errors_loss_fn=common.element_wise_squared_loss,
    train_step_counter=global_step
)
