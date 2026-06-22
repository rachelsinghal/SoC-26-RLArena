# Introduction to RL terminology 

## Insights and learnings from Sutton and Barto

The first chapter of the book introduced me to what Reinforcement Learning means, using a plethora of real-life analogies. It differentiates RL from supervised and unsupervised learning- there's no labelled training data provided like in supervised learning, neither is the goal finding a hidden pattern or structure in unlabelled data. Instead, RL is all about maximizing a measurable reward signal.

It also explains the tradeoff between exploration and exploitation in RL- exploratory moves are done to discover better alternatives for the future, whereas exploitation of gained experience is done to play optimally at present. There is no learning done in exploratory moves, because the "value" of a position can only be judged if the further play is optimally done.

Next we learn about elements of RL: a policy, a reward signal, a value function and a model of the environment. 
A policy is the mapping that determines the agent's behaviour as a function of the state of its environment. Instead of being deterministic, policies may specify probabilities for each action.
At each time step, the environment sends to the reinforcement learning agent a single number called the reward. The reward signal thus defines what are the good and bad events for the agent.
The value function provides a more long term outlook of what is good or bad for the agent, by analysing not only present but future rewards as well.

Finally, the book differentiates between evolutionary and value function methods. An example of Tic Tac Toe clarifies how values of previous states are updated as we encounter further states. 



