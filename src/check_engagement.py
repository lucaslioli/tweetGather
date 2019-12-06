import sys
import subprocess

if __name__ == '__main__':

    arg_names = ['command', 'user']
    args = dict(zip(arg_names, sys.argv))

    if 'user' not in args:
        args['user'] = ''

    rates = map(str, [0.002, 0.005, 0.006, 0.007, 0.008, 0.009, 0.010,
                      0.015, 0.020, 0.025, 0.030, 0.035, 0.040, 0.045,
                      0.050, 0.060, 0.070, 0.080, 0.090, 0.100, 0.150,
                      0.200, 0.250, 0.300, 0.350, 0.400, 0.450, 0.500,
                      0.600, 0.700, 0.800, 0.900, 1.000])

    for rate in rates:

        strout = ""

        command = ["python3", "src/prepare_dataset.py", "check", rate, args['user']]

        output = subprocess.check_output(command, encoding='utf8')

        if rate == '0.002':
            strout = "\n " + output[output.find('User'):output.find('TOTAL')-1]

        strout += output[1:output.find('User')]

        # Gets only the balanced instances information
        strout += output[output.find('TOTAL OF tweets'):output.find('TOTAL OF Popular')-2]

        print(strout)

    exit()
