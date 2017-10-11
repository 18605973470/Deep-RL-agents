
import tensorflow as tf

from Agent import Agent

from Displayer import DISPLAYER
from Saver import SAVER


if __name__ == '__main__':
    
    tf.reset_default_graph()

    with tf.Session() as sess:

        sess.run(tf.global_variables_initializer())

        agent = Agent(sess)
        SAVER.set_sess(sess)

        SAVER.load()

        print("Beginning of the run")
        try:
            agent.run()
        except KeyboardInterrupt:
            pass
        print("End of the run")
        SAVER.save(agent.total_steps)
        DISPLAYER.disp()

        agent.QValue()
        agent.stop()