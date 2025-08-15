from game import Game
from agent import Agent

def train(agent, num_episodes):
    env = Game()
    for episode in range(int(num_episodes)+1):
        state = env.get_state()
        done = False
        while not done:
            action = agent.get_action(state)
            reward, next_state, done = env.step(action)
            agent.update(state, action, reward, next_state)
            state = next_state
        agent.decay_epsilon()
        if episode%100 == 0:
            print(f"best score till episode {episode}: {env.best_score}")
        if episode%25 == 0:
            print(f"score of episode {episode}: {env.score}")
        env.restart()

def main():
    user_input = input("[0] Play\n[1] Reinforcement Learning\n")
    if int(user_input) == 0:
        game = Game()
        game.start()
    elif int(user_input) == 1:
        num_episodes = input("For how many episodes do you want to train the agent?\n")
        agent = Agent()
        train(agent, num_episodes)
        env = Game()
        env.rl_start(agent)

if __name__ == "__main__":
    main()