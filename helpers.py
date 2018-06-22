import numpy
from scipy import signal
import logging
from multiprocessing import Process


def time_delay_function_optimized(start, end, outs, multi):
    for idx in range(start, end):
        logging.info('Receiver '+str(idx+1)+' in action')

        c = signal.correlate(multi[0,][:, 0], multi[idx,][:, 0], "full")
        C, I = c.max(0), c.argmax(0)
        outs[idx] = ((float(len(c)) + 1.0) / 2.0 - I) / 44100.0


def per_delta(start, end, delta):
    curr = start
    while curr < end and curr + delta < end:
        yield (curr, curr + delta)
        curr += delta
    yield (curr, end)


def time_delay_function(x, y):
    c = signal.correlate(x[:, 0], y[:, 0], "full")
    C, I = c.max(0), c.argmax(0)
    out = ((float(len(c)) + 1.0) / 2.0 - I) / 44100.0
    return out

class ProcessParallel(object):
    """
    To Process the jobs in separate interpreters
    """
    def __init__(self):
        self.processes = []

    def add_task(self, job, arg):
        self.processes.append(Process(target=job, args=arg))

    def start_all(self):
        """
        Starts the functions process all together.
        """
        [process.start() for process in self.processes]

    def join_all(self):
        """
        Waits until all the processes executed.
        """
        [process.join() for process in self.processes]