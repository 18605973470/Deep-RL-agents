
from multiprocessing import cpu_count

DISPLAY = True


NB_ACTORS = cpu_count() - 2
DISCOUNT = 0.99

MEMORY_SIZE = 1000000
BATCH_SIZE = 64


CRITIC_LEARNING_RATE = 5e-4
ACTOR_LEARNING_RATE = 5e-4

UPDATE_TARGET_RATE = 0.2

UPDATE_TARGET_FREQ = 4
UPDATE_ACTORS_FREQ = 10

NOISE_SCALE = 0.3
NOISE_DECAY = 0.99


# Display settings
RENDER_FREQ = 1000
EP_REW_FREQ = 25
PLOT_FREQ = 500000
PERF_FREQ = 10000
