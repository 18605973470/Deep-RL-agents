
ENV = "LunarLander-v2"

LOAD = True
DISPLAY = True
GIF = True

CONV = False


DISCOUNT = 0.99
N_STEP_RETURN = 3
DISCOUNT_N = DISCOUNT**(N_STEP_RETURN-1)

FRAME_SKIP = 4


EPSILON_START = 0.8
EPSILON_STOP = 0.1
EPSILON_STEPS = 100000

LEARNING_RATE = 1e-4

BUFFER_SIZE = 100000
PRIOR_ALPHA = 0.5
PRIOR_BETA_START = 0.4
PRIOR_BETA_STOP = 1
PRIOR_BETA_STEPS = 100000

BATCH_SIZE = 32

# Number of episodes of game environment to train with
TRAINING_STEPS = 50000
PRE_TRAIN_STEPS = 1000

# Maximal number of steps during one episode
MAX_EPISODE_STEPS = 600
TRAINING_FREQ = 4

# Rate to update target network toward primary network
UPDATE_TARGET_RATE = 0.001
