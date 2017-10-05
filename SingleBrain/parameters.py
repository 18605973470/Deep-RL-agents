

ENV = 'SpaceInvaders-v0'

DISPLAY = True
LOAD = False

LIMIT_RUN_TIME = 120

THREADS = 4
OPTIMIZERS = 2
THREAD_DELAY = 0.001

GAMMA = 0.99

N_STEP_RETURN = 8
GAMMA_N = GAMMA ** N_STEP_RETURN

EPSILON_START = 0.8
EPSILON_STOP = .01
EPSILON_STEPS = 100000

MIN_BATCH = 32
LEARNING_RATE = 5e-3

LOSS_VALUE_REG = .5     # value regularization
LOSS_ENTROPY_REG = .01  # entropy regularization
