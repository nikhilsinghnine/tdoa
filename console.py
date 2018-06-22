from scikits.audiolab import wavread
import numpy
import math
from matplotlib import pyplot
from scipy import linalg
import time
from helpers import ProcessParallel
from multiprocessing import Array
import helpers
import logging

X_dict=[-2611.204, 1859.424, -169.088, 4642.943, 1826.389, 728.806, 4633.135]
Y_dict=[547.975, 4537.568, 2315.324, 5033.602, -64205.797, -57207.506, 5044.402]
Z_dict=[0.982, 6.256, 6.155, -0.916, -322.926, -254.013, 0.450]

X_dict=[x/1000.00 for x in X_dict]
Y_dict=[y/1000.00 for y in Y_dict]
Z_dict=[z/1000.00 for z in Z_dict]

speed=340.29

class Console:
    def __init__(self, audio, mic_amount, trials, proc_number):

        logging.info('Starting.')
        self.proc_numer = proc_number
        # the magic of preparing audio data; from numpy arrays to flatten list with removed duplicated elements
        self.wave = wavread(audio)[0]  # removing wav technical data; only audio data stays
        self.wave = [list(pair) for pair in self.wave]
        audio_data = numpy.array(self.wave)
        self.wave = list(audio_data.flatten())
        self.wave = self.wave[::2]
        self.wave = numpy.array(self.wave).reshape(-1, 1)

        self.scale = 0.8 / max(self.wave)
        self.wave = numpy.multiply(self.scale, self.wave)

        self.sample=float(wavread(audio)[1])
        print '\nSampling rate used: '+str(self.sample)

        self.trials = trials
        self.__microphone_amount = mic_amount

        self.subArrays_X=[]
        self.subArrays_Y=[]
        self.subArrays_Z=[]
        self.element=[0]
        self.generate_combinations(X_dict, Y_dict, Z_dict, 4) 
        #print self.subArrays
        X_receiver=[]
        Y_receiver=[]
        Z_receiver=[]
        indices_X=self.subArrays_X[0]
        indices_Y=self.subArrays_Y[0]
        indices_Z=self.subArrays_Z[0]
        for i,j,k in zip(indices_X, indices_Y, indices_Z):
            X_receiver.append(i)
            Y_receiver.append(j)
            Z_receiver.append(k)

        self.X = [X_receiver[i] for i in range(4)]
        self.Y = [Y_receiver[i] for i in range(4)]
        self.Z = [Z_receiver[i] for i in range(4)]

        self.sensor_positions = numpy.column_stack((self.X, self.Y, self.Z))
        self.true_positions = numpy.zeros((self.trials, 3))
        self.estimated_positions = numpy.zeros((self.trials, 3))

        self.distances = []
        self.time_delays = []
        self.padding = []

        print '\nReceiver Locations:'
        for i in range(len(self.X)):
        	print 'Receiver '+str(i+1)+': X: '+str(self.X[i])+'        Y: '+str(self.Y[i])+'     Z: '+str(self.Z[i])
        print '\n'
        logging.info('Inited core.')

    def generate_source_positions(self):
        logging.info('Generating sources positions.')

        x=[13970.04, 43271.75, 71300.97, 95219.61]      
        y=[-18557.80, -57444.36, -94639.05, -126379.45]
        z=[22270.68, 34057.40, 24218.86, 18483.85]

        x=[i/1000.00 for i in x]
        y=[j/1000.00 for j in y]
        z=[k/1000.00 for k in z]                     

        for i in range(self.trials):
            self.true_positions[i, 0] = x[i]
            self.true_positions[i, 1] = y[i]
            self.true_positions[i, 2] = z[i]

        print '\nObject Locations:'
        for i in range(self.trials):
            print 'Object '+str(i+1)+': X: '+str(self.true_positions[:,0][i])+'     Y: '+str(self.true_positions[:,1][i])+'     Z: '+str(self.true_positions[:,2][i])
        print '\n'

        logging.info('Generated sources positions.')

    def generate_distances(self):
        logging.info('Generating distances.')

        self.distances = numpy.zeros((self.trials, self.__microphone_amount))
        print '\n'
        for i in range(self.trials):
            for j in range(self.__microphone_amount):
                x1 = self.true_positions[i, 0]
                y1 = self.true_positions[i, 1]
                z1 = self.true_positions[i, 2]
                x2 = self.sensor_positions[j, 0]
                y2 = self.sensor_positions[j, 1]
                z2 = self.sensor_positions[j, 2]
                self.distances[i, j] = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
                print 'Distance between receiver '+str(j+1)+ ' and object '+str(i+1)+ ' is '+str(self.distances[i,j])
        print '\n'

        logging.info('Generated distances.')

    def prepare(self):
        logging.info('Preparing stage started.')

        self.time_delays = numpy.divide(self.distances, speed)
        self.padding = numpy.multiply(self.time_delays, 44100)
        print '\n'
        for i in range(len(self.time_delays[0])):
            print 'Pre Correlation: Time Difference between object '+str(1)+' and '+str(i+1)+': '+str(self.time_delays[0][i]-self.time_delays[0][0])
        print '\n'

        logging.info('Preparing stage ended.')

    def generate_signals(self):
        for i in range(self.trials):
            x = self.true_positions[i, 0]
            y = self.true_positions[i, 1]
            z = self.true_positions[i, 2]

            mic_data = [numpy.vstack((numpy.zeros((int(round(self.padding[i, j])), 1)), self.wave)) for j in
                        range(self.__microphone_amount)]
            lenvec = numpy.array([len(mic) for mic in mic_data])
            m = max(lenvec)
            c = numpy.array([m - mic_len for mic_len in lenvec])
            mic_data = [numpy.vstack((current_mic, numpy.zeros((c[idx], 1)))) for idx, current_mic in
                        enumerate(mic_data)]
            mic_data = [numpy.divide(current_mic, self.distances[i, idx]) for idx, current_mic in enumerate(mic_data)]
            multitrack = numpy.array(mic_data)

            logging.info('Prepared all data.')
            logging.info('Started source localization.')

            x, y, z = self.locate(self.sensor_positions, multitrack)

            logging.info('Localized source.')

            self.estimated_positions[i, 0] = x
            self.estimated_positions[i, 1] = y
            self.estimated_positions[i, 2] = z


    def generate_combinations(self,array_X, array_Y, array_Z, r):
        array1_X, array1_Y, array1_Z=[], [], []
        if r==len(array_X):
            if array_X not in self.subArrays_X:
                self.subArrays_X.append(array_X)
                return
            if array_Y not in self.subArrays_Y:
                self.subArrays_Y.append(array_Y)
                return
            if array_Z not in self.subArrays_Z:
                self.subArrays_Z.append(array_Z)
                return

        for item_X, item_Y, item_Z in zip(array_X, array_Y, array_Z):
            array1_X=array_X[:]
            array1_X.remove(item_X)
            array2_X=self.generate_combinations(array1_X, array1_Y, array1_Z, r)

            array1_Y=array_Y[:]
            array1_Y.remove(item_Y)
            array2_Y=self.generate_combinations(array1_X, array1_Y, array1_Z, r)

            array1_Z=array_Z[:]
            array1_Z.remove(item_Z)
            array2_Z=self.generate_combinations(array1_X, array1_Y, array1_Z, r)

            self.element[0]+=1
            if array2_X not in self.subArrays_X and array2_X:
                    self.subArrays_X.append(array2_X)
            if array2_Y not in self.subArrays_Y and array2_Y:
                    self.subArrays_Y.append(array2_Y)
            if array2_Z not in self.subArrays_Z and array2_Z:
                    self.subArrays_Z.append(array2_Z)


    def locate(self, sensor_positions, multitrack):
        s = sensor_positions.shape
        len = s[0]

        time_delays = numpy.zeros((len, 1))

        starts = time.time()

        if self.proc_numer == 1:
            for p in range(len):
                time_delays[p] = helpers.time_delay_function(multitrack[0,], multitrack[p,])
        else:
            pp = ProcessParallel()

            outs = Array('d', range(len))

            ranges = []

            for result in helpers.per_delta(0, len, len / self.proc_numer):
                ranges.append(result)

            for start, end in ranges:
                pp.add_task(helpers.time_delay_function_optimized, (start, end, outs, multitrack))

            pp.start_all()
            pp.join_all()
            print '\n'
            for idx, res in enumerate(outs):
                time_delays[idx] = res
                print 'Post Correlation: Time delay between object number '+str(1)+' and '+str(idx+1)+': '+str(time_delays[idx])
            print '\n'

        ends = time.time()

        logging.info('%.15f passed for trial.', ends - starts)

        Amat = numpy.zeros((len, 1))
        Bmat = numpy.zeros((len, 1))
        Cmat = numpy.zeros((len, 1))
        Dmat = numpy.zeros((len, 1))

        for i in range(2, len):
            x1 = sensor_positions[0, 0]
            y1 = sensor_positions[0, 1]
            z1 = sensor_positions[0, 2]
            x2 = sensor_positions[1, 0]
            y2 = sensor_positions[1, 1]
            z2 = sensor_positions[1, 2]
            xi = sensor_positions[i, 0]
            yi = sensor_positions[i, 1]
            zi = sensor_positions[i, 2]
            Amat[i] = (1 / (speed * time_delays[i])) * (-2 * x1 + 2 * xi) - (1 / (speed * time_delays[1])) * (
                -2 * x1 + 2 * x2)
            Bmat[i] = (1 / (speed * time_delays[i])) * (-2 * y1 + 2 * yi) - (1 / (speed * time_delays[1])) * (
                -2 * y1 + 2 * y2)
            Cmat[i] = (1 / (speed * time_delays[i])) * (-2 * z1 + 2 * zi) - (1 / (speed * time_delays[1])) * (
                -2 * z1 + 2 * z2)
            Sum1 = (x1 ** 2) + (y1 ** 2) + (z1 ** 2) - (xi ** 2) - (yi ** 2) - (zi ** 2)
            Sum2 = (x1 ** 2) + (y1 ** 2) + (z1 ** 2) - (x2 ** 2) - (y2 ** 2) - (z2 ** 2)
            Dmat[i] = speed * (time_delays[i] - time_delays[1]) + (1 / (speed * time_delays[i])) * Sum1 - (1 / (
                speed * time_delays[1])) * Sum2

        M = numpy.zeros((len + 1, 3))
        D = numpy.zeros((len + 1, 1))
        for i in range(len):
            M[i, 0] = Amat[i]
            M[i, 1] = Bmat[i]
            M[i, 2] = Cmat[i]
            D[i] = Dmat[i]

        M = numpy.array(M[2:len, :])
        D = numpy.array(D[2:len])

        D = numpy.multiply(-1, D)

        Minv = linalg.pinv(M)

        T = numpy.dot(Minv, D)
        x = T[0]
        y = T[1]
        z = T[2]

        return x, y, z

    def draw_plot(self):
        pyplot.plot(self.true_positions[:, 0], self.true_positions[:, 1], 'bd', label='True position')
        pyplot.plot(self.estimated_positions[:, 0], self.estimated_positions[:, 1], 'r+', label='Estimated position')
        pyplot.legend(loc='upper right', numpoints=1)
        pyplot.xlabel('X coordinate of target')
        pyplot.ylabel('Y coordinate of target')
        pyplot.title('TDOA Hyperbolic Localization')
        pyplot.axis([-100, 100, -100, 100])
        pyplot.show()
