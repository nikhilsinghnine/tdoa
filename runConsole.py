
from console import Console
from multiprocessing import freeze_support, cpu_count
import argparse
import logging

X_dict=[-2611.204, 1859.424, -169.088, 4642.943, 1826.389, 728.806, 4633.135 , 5891.094, 4633.135, 5891.094]
Y_dict=[547.975, 4537.568, 2315.324, 5033.602, -64205.797, -57207.506, 5044.402, 684.936, 5044.402, 684.936]
Z_dict=[0.982, 6.256, 6.155, -0.916, -322.926, -254.013, 0.450, 23.875, 0.450, 23.875]

X_dict=[x/1000.00 for x in X_dict]
Y_dict=[y/1000.00 for y in Y_dict]
Z_dict=[z/1000.00 for z in Z_dict]

speed=340.29

if __name__ == '__main__':
    freeze_support()

    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--mic_amount", type=int, help="microphone amount")
    parser.add_argument("-p", "--proc_number", type=int, help="process number")
    parser.add_argument("-t", "--trials", type=int, help="trials number")
    parser.add_argument("-f", "--file", type=str, help="file name")
    parser.add_argument("-l", "--log_file", type=str, help="log file")

    args = parser.parse_args()

    if args.log_file:
        logging.basicConfig(format='%(levelname)s, PID: %(process)d, %(asctime)s:\t%(message)s', level=logging.INFO)
    else:
        logging.basicConfig(format='%(levelname)s, PID: %(process)d, %(asctime)s:\t%(message)s', filename=args.log_file, level=logging.INFO)

    if args.proc_number:
        if args.proc_number <= 0:
            raise ValueError('proc_number can''t be less then zero.')
        cores_to_use = args.proc_number
    else:
        cores_to_use = cpu_count()

    console = Console(args.file, mic_amount=args.mic_amount, trials=args.trials, proc_number=cores_to_use)

    console.generate_source_positions()
    console.generate_distances()
    console.prepare()
    console.generate_signals()

    for trial_number in range(console.trials):
        logging.info('\nTrial number: %d', trial_number + 1)

        logging.info('Error X = %.15f, Error Y = %.15f, Error Z = %.15f', float(console.true_positions[trial_number][0]-console.estimated_positions[trial_number][0]),
                    float(console.true_positions[trial_number][1]-console.estimated_positions[trial_number][1]),
                    float(console.true_positions[trial_number][2]-console.estimated_positions[trial_number][2]))

        logging.info('Error in distance: '+str((float(console.true_positions[trial_number][0]-console.estimated_positions[trial_number][0])**2+
                    float(console.true_positions[trial_number][1]-console.estimated_positions[trial_number][1])**2+
                    float(console.true_positions[trial_number][2]-console.estimated_positions[trial_number][2])**2)**(0.5)))

        logging.info('Estimated X = %.15f, Estimated Y = %.15f, Estimated Z = %.15f', float(console.estimated_positions[trial_number][0]),
                    float(console.estimated_positions[trial_number][1]),
                    float(console.estimated_positions[trial_number][2]))

        logging.info('True X = %.15f, True Y = %.15f, True Z = %.15f', float(console.true_positions[trial_number][0]),
                    float(console.true_positions[trial_number][1]),
                    float(console.true_positions[trial_number][2]))

    #console.draw_plot()
