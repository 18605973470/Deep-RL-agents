
import random
import numpy as np
import tensorflow as tf

from Environment import Environment
from baselines.deepq.replay_buffer import PrioritizedReplayBuffer
from QNetwork import QNetwork

from Displayer import DISPLAYER
from Saver import SAVER
import parameters


def updateTargetGraph(tfVars):
    total_vars = len(tfVars)
    op_holder = []
    tau = parameters.UPDATE_TARGET_RATE
    for idx, var in enumerate(tfVars[0:total_vars // 2]):
        op_holder.append(tfVars[idx + total_vars // 2].assign(
            (var.value() * tau) +
            ((1 - tau) * tfVars[idx + total_vars // 2].value())))
    return op_holder


def update_target(op_holder, sess):
    for op in op_holder:
        sess.run(op)


class Agent:

    def __init__(self, sess):
        print("Initializing the agent...")
        self.sess = sess
        self.env = Environment()
        self.state_size = self.env.get_state_size()
        self.action_size = self.env.get_action_size()

        print("Creation of the main QNetwork")
        self.mainQNetwork = QNetwork(self.state_size, self.action_size, 'main')
        print("Creation of the target QNetwork")
        self.targetQNetwork = QNetwork(self.state_size, self.action_size,
                                       'target')

        self.buffer = PrioritizedReplayBuffer(parameters.BUFFER_SIZE,
                                              parameters.PRIOR_ALPHA)

        self.epsilon = parameters.EPSILON_START
        self.epsilon_decay = (parameters.EPSILON_START -
                              parameters.EPSILON_STOP) \
            / parameters.EPSILON_STEPS

        self.beta = parameters.PRIOR_BETA_START
        self.beta_incr = (parameters.PRIOR_BETA_STOP -
                          parameters.PRIOR_BETA_START) \
            / parameters.PRIOR_BETA_STEPS

        trainables = tf.trainable_variables()
        self.update_target_ops = updateTargetGraph(trainables)

    def run(self):

        self.total_steps = 0
        training = False
        for i in range(parameters.TRAINING_STEPS):
            state = self.env.reset()
            s = [0] * self.state_size[0]
            s[state] = 1
            done = False
            episode_reward = 0
            step = 0

            while step < parameters.MAX_EPISODE_STEPS and not done:

                if random.random() < self.epsilon or \
                        self.total_steps < parameters.PRE_TRAIN_STEPS:
                    a = random.randint(0, self.action_size - 1)
                else:
                    a = self.sess.run(self.mainQNetwork.predict,
                                      feed_dict={self.mainQNetwork.inputs: [s]})
                    a = a[0]

                if self.epsilon > parameters.EPSILON_STOP:
                    self.epsilon -= self.epsilon_decay

                R = 0
                for _ in range(parameters.FRAME_SKIP):
                    state, r, done, info = self.env.act(a)
                    s_ = [0] * self.state_size[0]
                    s_[state] = 1
                    R += r
                    if done:
                        break

                self.buffer.add(s, a, R, s_, done)

                episode_reward += R
                s = s_

                step += 1
                self.total_steps += 1

                if training and self.total_steps > parameters.PRE_TRAIN_STEPS:
                    training = False
                    print("End of the pre-training")

                if self.total_steps > parameters.PRE_TRAIN_STEPS and \
                        self.total_steps % parameters.TRAINING_FREQ == 0:
                    train_batch = self.buffer.sample(parameters.BATCH_SIZE,
                                                     self.beta)

                    feed_dict = {self.mainQNetwork.inputs: train_batch[3]}
                    mainQaction = self.sess.run(self.mainQNetwork.predict,
                                                feed_dict=feed_dict)

                    feed_dict = {self.targetQNetwork.inputs: train_batch[3]}
                    targetQvalues = self.sess.run(self.targetQNetwork.Qvalues,
                                                  feed_dict=feed_dict)

                    # Done multiplier :
                    # equals 0 if the episode was done
                    # equals 1 else
                    done_multiplier = -1 * (train_batch[4] - 1)
                    doubleQ = targetQvalues[
                        range(parameters.BATCH_SIZE), mainQaction]
                    targetQvalues = train_batch[2] + \
                        parameters.DISCOUNT * doubleQ * done_multiplier

                    feed_dict = {self.mainQNetwork.inputs: train_batch[0],
                                 self.mainQNetwork.Qtarget: targetQvalues,
                                 self.mainQNetwork.actions: train_batch[1]}
                    _ = self.sess.run(self.mainQNetwork.train,
                                      feed_dict=feed_dict)

                    update_target(self.update_target_ops, self.sess)

            # Save the model
            if (i + 1) % 10000 == 0:
                print(episode_reward)
                SAVER.save(i)

            if self.total_steps > parameters.PRE_TRAIN_STEPS:
                DISPLAYER.add_reward(episode_reward)

    def QValue(self):
        print("QValues : ")
        for state in range(self.state_size[0]):
            s = [0]*self.state_size[0]
            s[state] = 1
            qval = self.sess.run(self.mainQNetwork.Qvalues,
                              feed_dict={self.mainQNetwork.inputs: [s]})
            print(qval)

    def play(self, number_run):
        print("Playing for", number_run, "runs")

        self.env.set_render(True)
        try:
            for _ in range(number_run):

                state = self.env.reset()
                s = [0] * self.state_size[0]
                s[state] = 1
                episode_reward = 0
                done = False

                while not done:
                    a = self.sess.run(self.mainQNetwork.predict,
                                      feed_dict={self.mainQNetwork.inputs: [s]})
                    a = a[0]
                    state, r, done, info = self.env.act(a)
                    s = [0] * self.state_size[0]
                    s[state] = 1

                    episode_reward += r

                print("Episode reward :", episode_reward)

        except KeyboardInterrupt as e:
            pass

        finally:
            self.env.set_render(False)
            print("End of the demo")
            self.env.close()

    def stop(self):
        self.env.close()
