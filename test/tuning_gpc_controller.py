#!/usr/bin/env python2.7
from controller.dynamic_model import *
from controller.soloway_nr import *
from gym.block_gym import *
from collections import deque
from scipy import signal as sig
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
import time, os

plt.style.use('seaborn')
model_filename = str(os.environ['HOME']) + '/gpc_controller/test/sys_id.hdf5'

def verbose0(x, y, z, w, k):
    print "-----------------------------------------------------"
    print "GPC: Target: ", x
    print "GPC: P. State: ", y
    print "GPC: Act. State: ", z
    print "GPC: u_optimal", w
    print "GPC: Cost: ", k

NUM_EXPERIMENTS = 1
NUM_TIMESTEPS = 500
NNP = NeuralNetworkPredictor(model_file = model_filename, N1 = 0, \
                N2 = 10, Nu = 1, nd = 3, dd = 3, K = 10, \
                    lambd = np.array([[1e-5], [1e-3]]), \
                        y0 = [0.02, -0.05, 0.05], \
                            u0 = [0.0, -50.0], s = 1e-10, b = 5e2, r = 5e2)

NR_opt, Block = SolowayNR(cost = NNP.Cost, d_model = NNP), BlockGym(vrpn_ip = "192.168.50.24:3883")

Block.reset()
neutral_point = Block.get_state()
NNP.y0 = neutral_point
verbose = 1

print NNP.model.summary()

def custom_loss(y_true, y_pred):
    pass

#Block.stretch() # stretch block for better signal readings before calibrating
#Block.get_signal_calibration() # calibrate signal of the block
Block.calibration_max = np.array([1, 335, 120,1,1, 1, 166,9,1,50,1])

u_optimal_old = np.reshape([0., -50.]*NNP.Nu, (-1, 2))
new_state_new = Block.get_state()
del_u = np.zeros(u_optimal_old.shape)
elapsed , u_optimal_list, ym, yn, predicted_, actual_ = [],[],[],[],[],[]
u_deque, y_deque = deque(), deque()

for _ in range(NNP.nd):
    u_deque.append([0.0, -50.0])
for _ in range(NNP.dd):
    y_deque.append(Block.get_state())

u_action, predicted_states = np.array([0.0, -50.0]), np.array(new_state_new)
try:
    for e in range(NUM_EXPERIMENTS):
        print "----------------------------"
        print "         NEW EXPERIMENT # ", e
        print "____________________________"
        pred_exp, actual_exp, yn_exp, ym_exp, elapsed_exp, u_exp = [], [], [], [], [], []

        for n in range(NUM_TIMESTEPS):
            seconds = time.time()
            signal = np.divide(Block.get_observation(), Block.calibration_max, dtype = np.float64).tolist()
            NNP.yn = []
            for ii in range(NNP.K):
                neural_network_input = np.array((np.array(list(u_deque))/100.).flatten().tolist() + \
                                                    np.array(list(y_deque)).flatten().tolist() + \
                                                    signal).reshape(1, -1)
                predicted_states = NNP.predict(neural_network_input).flatten()
                NNP.yn += [predicted_states]
                if ii > NNP.dd:
                    y_deque.pop()
                    y_deque.appendleft(predicted_states.tolist())

            pred_exp += [predicted_states]

            omega, amplitude, initial_angle, circle_center = 500,  0.025/2., 0.0, neutral_point

            NNP.ym = np.tile([circle_center[0],  \
                                        circle_center[1] + amplitude * np.cos(2*np.pi * n / omega),
                                        circle_center[2] + amplitude/2. * np.sin(2*np.pi * n / omega)], (NNP.K, 1))

            new_state_old = new_state_new

            u_optimal, del_u,  _ = NR_opt.optimize(u = u_optimal_old, \
                                        maxit = 3, rtol = 1e-8, verbose = False)

            u_action = u_optimal[0, :].tolist()

            SCALING0 = 1
            SCALING1 = 1

            u_action[0] = np.clip(u_action[0]*SCALING0, -100, 100)
            u_action[1] = np.clip(u_action[1]*SCALING1, -100, 60)

            del_u_action = del_u[0, :].tolist()
            actual_st = Block.get_state()

            if verbose == 0:
                verbose0(NNP.ym, NNP.yn, np.array(actual_st), u_action, NNP.compute_cost())
            if verbose == 1:
                print "GPC: u_optimal ", u_action

            NNP.update_dynamics(u_action, del_u_action, predicted_states.tolist(), NNP.ym[0, :].tolist())
            u_optimal_old = u_optimal
            Block.step(action = u_action)
            u_deque.pop()
            y_deque.pop()
            u_deque.appendleft(u_action)
            y_deque.appendleft(predicted_states.tolist())

            ym_exp += [NNP.ym[0, :]]
            yn_exp += [predicted_states]
            elapsed_exp += [time.time() - seconds]

            if verbose == 0:
                print "GPC: elapsed time: ", elapsed_exp[-1]

            u_exp += [u_action]
            actual_exp += [(np.array(Block.get_state())).tolist()]

        predicted_ += [pred_exp]
        actual_ += [actual_exp]
        yn += [yn_exp]
        ym += [ym_exp]
        u_optimal_list+=[u_exp]
        elapsed+=[elapsed_exp]
        u_optimal_old = np.reshape([0., -50.]*NNP.Nu, (-1, 2))
        Block.reset()
    """
        ----------------> PLOTTING <--------------------------
    """

    Block.reset()
    ym = 1000*np.reshape(ym, (NUM_EXPERIMENTS,-1, 3))
    yn = 1000*np.reshape(yn, (NUM_EXPERIMENTS, -1, 3))

    predicted_ = 1000*np.reshape(predicted_, (NUM_EXPERIMENTS, -1, 3))
    actual_ = 1000*np.reshape(actual_, (NUM_EXPERIMENTS,-1, 3))
    u_optimal_list = np.reshape(u_optimal_list, (NUM_EXPERIMENTS, -1, 2))
    neutral_point = 1000*neutral_point
    print "Block calibration vector: ", Block.calibration_max
    labels = ['x', 'y', 'z', 'u']
    plt.figure()
    AXIS = 0
    timesteps = range(max(yn.shape))
    for i in range(3):
        plt.subplot(3, 1, i+1)
        plt.plot(np.mean(ym, axis = AXIS)[:, i], color = '#d3d3d3', linestyle = 'dashed', label = 'target')
        plt.plot(np.mean(yn, axis = AXIS)[:, i], '#bfcbc5', label = 'predicted state')
        plt.fill_between(timesteps, np.mean(yn, axis = AXIS)[:, i] - np.std(yn, axis = AXIS)[:, i] ,\
                            np.mean(yn, axis = AXIS)[:, i] + np.std(yn, axis = AXIS)[:, i], \
                                color = '#bfcbc5', alpha = 0.5)
        plt.plot(np.mean(actual_, axis = AXIS)[:, i], color = 'goldenrod', label = 'actual state') # only 0 and 2

        plt.fill_between(timesteps, np.mean(actual_, axis = AXIS)[:, i] - np.std(actual_, axis = AXIS)[:, i],\
                                        np.mean(actual_, axis = AXIS)[:, i] + np.std(actual_, axis = AXIS)[:, i],\
                                            color = 'goldenrod', alpha = 0.5)

        plt.ylim([-0.1*1000, 0.09*1000])
        plt.legend()
        plt.ylabel(str(labels[i]) + ' [mm]')
        plt.plot(1000*neutral_point[i], marker = 'h')
        if i==2:
            plt.xlabel('timesteps')
        if i==0:
            plt.title("Changes in States with respect to Timesteps")
    plt.show()

    max_input = np.max(np.max(u_optimal_list))
    min_input = np.min(np.min(u_optimal_list))
    plt.figure()
    for i in range(2):
        plt.subplot(2, 1, i+1)
        plt.plot(np.mean(u_optimal_list, axis =AXIS)[:, i], color = 'slateblue', label = r'$u_{' + str(i) + "}$" )
        plt.fill_between(timesteps, np.mean(u_optimal_list, axis = AXIS)[:, i] -  np.std(u_optimal_list, axis = AXIS)[:, i],\
                                        np.mean(u_optimal_list, axis = AXIS)[:, i] + np.std(u_optimal_list, axis = AXIS)[:, i],\
                                            color = 'slateblue', alpha = 0.3, label = r"$2\sigma$")


        plt.legend()
        plt.ylim([min_input, max_input])
        plt.ylabel(str(labels[-1]) + ' [degrees]')
        if i == 0:
            plt.title('Changes in Inputs with respect to Timesteps')
    plt.xlabel('timesteps')
    plt.show()

    neutral_point = np.array(neutral_point).reshape(-1, 3)

    fig = plt.figure()
    m_predicted_ = 1000*np.mean(predicted_, axis = AXIS)
    m_ym = np.mean(ym, axis = AXIS)
    m_actual_ = np.mean(actual_, axis = AXIS)
    ax = Axes3D(fig)
    ax.plot3D(m_predicted_[:, 0],m_predicted_[:, 1], m_predicted_[:, 2],color = 'c',  linewidth = 1, alpha = 0.9, label = 'estimated position')
    ax.plot3D(m_ym[:, 0], m_ym[:, 1], m_ym[:, 2], color = 'grey',linestyle = 'dashed',  linewidth = 1, alpha = 1, label = 'target')
    ax.plot3D(m_actual_[:, 0], m_actual_[:, 1], m_actual_[:, 2], \
                        linewidth = 1, color = 'goldenrod', alpha = 1, label = 'actual position')
    ax.set_xlim(-0.1*1000, .1*1000)
    ax.set_ylim(-.1*1000, .1*1000)
    ax.set_zlim(-.1*1000, .1*1000)
    plt.legend()
    plt.xlabel('x[mm]')
    plt.ylabel('y[mm]')
    plt.title('Target Position vs. Controlled Positions')
    plt.show()
except Exception as e:
    Block.reset()
    print str(e)
    Block.reset()
