# Import libraries
import sys
import time

# Import class files
from person import Person
from simulation import Simulation
import mode

def setting(N, T, alpha, beta, gamma, phi, delta, phi_V, phi_T, immune_time, verbose_mode):
    info = input('Information about the parameters? [y/n] ').lower()
    print()
    if info == 'y':
        info_summ()
    print('Leave blank if not changing the value(s).')
    N_temp = input('N >>> ')
    N = set_correct_para(N_temp, N, pos=True)
    T_temp = input('T >>> ')
    T = set_correct_para(T_temp, T, pos=True)
    alpha_temp = input('alpha >>> ')
    alpha = set_correct_epi_para(alpha_temp, alpha)
    beta_temp = input('beta >>> ')
    beta = set_correct_epi_para(beta_temp, beta)
    gamma_temp = input('gamma >>> ')
    gamma = set_correct_epi_para(gamma_temp, gamma)
    phi_temp = input('phi >>> ')
    phi = set_correct_epi_para(phi_temp, phi)
    delta_temp = input('delta >>> ')
    delta = set_correct_epi_para(delta_temp, delta)
    cmd = input('Other parameters? [y/n] ')
    if cmd == 'y':
        N, T, alpha, beta, gamma, phi, delta, phi_V, phi_T, immune_time, verbose_mode = setting_other(N, T, alpha, beta, gamma, phi, delta, phi_V, phi_T, immune_time, verbose_mode)
    population = Person.make_population(N)
    return N, T, alpha, beta, gamma, phi, delta, phi_V, phi_T, immune_time, verbose_mode

def setting_other(N, T, alpha, beta, gamma, phi, delta, phi_V, phi_T, immune_time, verbose_mode):
    print('\n Wear-off parameters \n')
    phi_V_temp = input('Vaccine: ')
    phi_V = set_correct_epi_para(phi_V_temp, phi_V)
    phi_T_temp = input('Treatment: ')
    phi_T = set_correct_epi_para(phi_T_temp, phi_T)
    print('\n Infection related \n')
    immune_time_temp = input('Immune time (days): ')
    immune_time = set_correct_epi_para(immune_time_temp, immune_time)
    # if 1 in modes:
    #     print('\nYou have initiated mode 1 \n')
    cmd = input('Verbose mode? [y/n]')
    if cmd == 'y':
        verbose_mode = True
    elif cmd == 'n':
        verbose_mode = False
    return N, T, alpha, beta, gamma, phi, delta, phi_V, phi_T, immune_time, verbose_mode

def summary():
    print('N: {}'.format(N))
    print('T: {}'.format(T))
    print('===== SIR Rate =====')
    print('alpha: {}'.format(alpha))
    print('beta: {}'.format(beta))
    print('gamma: {}'.format(gamma))
    print('phi: {}'.format(phi))
    print('delta: {}'.format(delta))
    cmd = input('Show other epidemic paremeters? [y/n] ')
    if cmd == 'y':
        print('immune time = {}'.format(immune_time))
    info = input('Information about the parameters? [y/n] ').lower()
    if info == 'y':
        info_summ()
    if len(modes) > 0:
        info = input('There are customised settings. View them? [y/n] ')
        if info == 'y':
            for mode in modes.values():
                print(mode.__dict__)
    print()

def info_summ():
    print('N - Number of simulated agents.')
    print('T - Time steps/ period of simulation.')
    print('Alpha - Adoption of vaccination/ PrEP (willingness).')
    print('Beta - Infection rate.')
    print('Gamma - Recovery rate.')
    print('Phi - Protection wear off rate.')
    print('Delta - Removal rate.')

def help():
    print('LOOK - View partner network.')
    print('MODE - Change mode settings.')
    print('RUN/ START - Start the simulation.')
    print('SETTING - Set simulation settings.')
    print('OTHER SETTING - Set auxiliary simulation parameters.')
    print('SUMMARY - Print the simulation parameters.')
    print('QUIT/ Q - Quit the software.')

def usage():
    print('Usage: python3 main.py [(N) (T) (α) (β) (γ) (φ) (δ)] ...\n\
    [-m  <modes_config>] [-f (filename)] [-verbose | --v] [run]\n')
    print('-immune_time \t Immune time after recovered, in days.')
    print('-m \t\t Mode')
    print('    --1 \t Living in city/ rural.')
    print('    --10 \t Type of vaccine.')
    print('    --11 \t Stop transmissability/ reduce severity.')
    print('    --11 \t Initial infection by number.')
    print('-h \t\t Usage.')
    print('run \t\t Run simulation, last argument.')

def correct_bool_para(b):
    '''
    Convert the parameters into boolean.

    Parameters
    ----------
    b: bool
        Input.
    '''
    try:
        if b == 'True':
            b_bool = True
        elif b == 'False':
            b_bool = False
        else:
            raise ValueError ('Invalid boolean input. Please check your inputs. Default: True')
        return b_bool
    except ValueError:
        b_bool = True
        return b_bool

def set_correct_bool_para(b, B):
    '''
    Convert the parameters into integers. If input is blank then do nothing.

    Parameters:
    p -- string input.
    P -- original value.
    pos -- If the parameter is positive number.
    '''
    if b == '':
        return B
    else:
        return correct_bool_para(b)

def correct_para(p, pos=False):
    '''
    Convert the parameters into integers.

    Parameters
    p -- input.
    - pos: If the parameter is positive number.
    '''
    try:
        p_num = int(p)
        if pos == True and p_num < 1:
            p_num = 1
        return p_num
    except ValueError:
        p_num = 1
        return p_num

def set_correct_para(p, P, pos=False):
    '''
    Convert the parameters into integers. If input is blank then do nothing.

    Parameters:
    p -- string input.
    P -- original value.
    pos -- If the parameter is positive number.
    '''
    if p == '':
        return P
    else:
        return correct_para(p, pos=False)

def correct_epi_para(p):
    '''
    Convert epidemic parameters into floats.

    Parameters
    - p: Epidemic rate, positive decimal less than 1.
    '''
    try:
        p_num = float(p)
        if p_num < 0 or p_num > 1:
            p_num = 0
            print('Please check your inputs and change them in SETTING.')
        return p_num
    except ValueError:
        p_num = 0
        print('Please check your inputs and change them in SETTING.')
        return p_num

def set_correct_epi_para(p, P):
    '''
    Convert the parameters into integers. If input is blank then do nothing.

    Parameters:
    p -- string input.
    P -- original value.
    pos -- If the parameter is positive number.
    '''
    if p == '':
        return P
    else:
        return correct_epi_para(p)

def set_mode(mode):
    cmd = ''
    while cmd != 'y':
        print('Select the following options:')
        print('01: Living in city/ rural [{}]'.format(mode01.flag))
        print('10: Type of vaccine [{}]'.format(mode10.flag))
        print('11: Initial infection by number [{}]'.format(mode11.flag))
        print('Input number codes to change the options.')
        mode_input = input('> ')
        print(mode_input)
        mode = mode_settings(mode_input, mode)
        cmd = input('Return to main menu? [y/n] ')
    return mode

def mode_settings(cmd, mode=None):
    cmd = cmd.split(' ')
    if cmd == ['']:
        # If empty response, then leave prematurely.
        return mode
    rv_modes = []
    if '-dp' in cmd:
        removal_idx = cmd.index('-dp')
    print('Adding: ')
    if '-dp' in cmd:
        print(cmd[:removal_idx])
        print('Removing')
        print(cmd[removal_idx+1:])

        rv_modes = cmd[removal_idx+1:]
        cmd = cmd[:removal_idx]
    else:
        print(cmd)
    if len(cmd) > 0 and '-dp' not in cmd:
        for i in range(len(cmd)):
            try:
                int(cmd[i])
            except ValueError:
                print('Wrong data type for mode, please check your inputs.')
                continue
            if int(cmd[i]) == 1:
                mode01()
                if mode01.flag == 'X':
                    mode[1] = mode01
                else:
                    mode.pop(1)
            elif int(cmd[i]) == 10:
                mode10()
                if mode10.flag == 'X':
                    mode[10] = mode10
                else:
                    mode.pop(10)
            elif int(cmd[i]) == 11:
                mode11()
                if mode11.flag == 'X':
                    mode[11] = mode11
                else:
                    mode.pop(11)
    # Remove modes (Check if the modes itself overwrites basic settings)
    if len(rv_modes) > 0:
        for mode_opt in rv_modes:
            try:
                print(mode[int(mode_opt)].flag)
                mode[int(mode_opt)].drop_flag()
            except KeyError:
                continue
            except ValueError:
                continue
    return mode

# print('  ==========================================  \n\n')
# print('               Virus Spread Model             \n\n')
# print('  ==========================================  ')
# print()
# # Express mode: Call usage information
# if len(sys.argv) == 2 and (sys.argv[1] == '-help' or sys.argv[1] == '-h'):
#     usage()
#     quit()

# if len(sys.argv) == 1:
#     N = input('Number of people (N): ')
#     N = correct_para(N, pos=True)
#     T = input('Simulation time (T): ')
#     T = correct_para(T)
#     alpha = input('Adoption rate (alpha): ')
#     alpha = correct_epi_para(alpha)
#     beta = input('Infection rate (beta): ')
#     beta = correct_epi_para(beta)
#     gamma = input('Recovery rate (gamma): ')
#     gamma = correct_epi_para(gamma)
#     phi = input('Rate to resuscept (phi): ')
#     phi = correct_epi_para(phi)
#     delta = input('Removal rate (delta): ')
#     delta = correct_epi_para(delta)
# elif len(sys.argv) > 1:
#     print('Using pre-defined inputs. ')
#     try:
#         N = correct_para(sys.argv[1], pos=True)
#         T = correct_para(sys.argv[2])
#         alpha = correct_epi_para(sys.argv[3])
#         beta = correct_epi_para(sys.argv[4])
#         gamma = correct_epi_para(sys.argv[5])
#         phi = correct_epi_para(sys.argv[6])
#         delta = correct_epi_para(sys.argv[7])
#     except:
#         print('Exception encountered. Leaving program...')
#         print('Usage: python3 main.py [(N) (T) (α) (β) (γ) (φ) (δ)] ...\n[-m <modes_config>] [-f (filename)] [run]\n')
#         quit()
# print()

# '''
# Set initial variables
# '''
# phi_V = phi
# phi_T = 0.95
# immune_time = 70

# verbose_mode = False  # Need to put here for initiating other objects (nwk and person if needed).
# population = Person.make_population(N)
# filename = ''  # Default file name to export (.csv). Change when use prompt 'export' cmd.

# # mode_master_list = []
# # All objects should add into mode_master_list
# mode01 = mode.Mode01(population)
# mode10 = mode.Mode10(population, phi, beta)
# mode11 = mode.mode11(population)

# mode_master_list = [mode01, mode10, mode11]


# modes = {}

# '''
# Express mode

# Loads the settings prior to the run. Optional keyword 'run' to run the simulation automatically.
# '''

# # Check if mode exists
# for i in range(len(sys.argv)):
#     try:
#         if sys.argv[i] == '-immune_time':
#             immune_time_temp = sys.argv[i+1]
#             immune_time = set_correct_para(immune_time_temp, immune_time, pos=True)
#         elif sys.argv[i] == '-verbose' or sys.argv[i] == '--v':
#             verbose_mode = True
#         elif sys.argv[i] == '-m':
#             for j in range(i+1,len(sys.argv)):
#                 # Skip at other options
#                 if sys.argv[j][:2] == '--':
#                     mode_flag = int(sys.argv[j][2:])
#                     print('Loading mode: {}'.format(mode_flag))

#                     # Loop through config values
#                     for k in range(j+1,len(sys.argv)):
#                         if sys.argv[k][0] == '-' and sys.argv[k][1].isalpha():
#                             break
#                         if sys.argv[k][:2] == '--':
#                             break

#                         # Set up individual modes
#                         if mode_flag == 1:
#                             # Placeholder
#                             if sys.argv[k][:3] == '*b=':
#                                 mode01_b_config = sys.argv[k][3:].split(',')
#                                 b_c = float(mode01_b_config[0])
#                                 b_r = float(mode01_b_config[1])
#                                 mode01.set_beta(0,b_c)
#                                 mode01.set_beta(1,b_r)
#                             elif sys.argv[k][:3] == '*p=':
#                                 mode01_p_config = sys.argv[k][3:].split(',')
#                                 w_c = float(mode01_p_config[0])
#                                 w_r = float(mode01_p_config[1])
#                                 mode01.set_weight(w_c, w_r)

#                             mode01.assign_regions()
#                             mode01.raise_flag()
#                             if mode01.flag == 'X':
#                                 modes[1] = mode01
#                             else:
#                                 mode.pop(1)
#                         elif mode_flag == 10:
#                             if sys.argv[k][:6] == '*mode=':
#                                 modes[10].type = modes[10].check_input(sys.argv[k][6:])
#                             if mode10.flag == 'X':
#                                 modes[10] = mode10
#                             else:
#                                 modes.pop(10)
#                         elif mode_flag == 11:
#                             if sys.argv[k][:4] == '*Ii=':
#                                 Ii_temp = sys.argv[k][4:]
#                                 mode11.init_infection = mode11.set_init_infection(Ii_temp)
#                             mode11.raise_flag()
#                             if mode11.flag == 'X':
#                                 modes[11] = mode11
#                             else:
#                                 mode.pop(11)
#                         else:
#                             print('Warning: Mode not detected. ')

#                     continue
#                 if sys.argv[j][0] == '-' and sys.argv[j][1].isalpha():
#                     break
#                 if sys.argv[j] == 'run':
#                     break
#                 # print(mode_flag, '*'+str(argv[j]))
#     except ValueError:
#         print('Invalid input. Check your arguments. ')
#         continue
#     except IndexError:
#         break

# if sys.argv[-1] == 'run':
#     print('===== Simulation Running =====')
#     # Поменять здесь 
#     current_run = Simulation(population, T, population, alpha, beta, gamma, phi, delta, filename, immune_time, verbose_mode)
#     # Load modes
#     current_run.load_modes(modes)
#     if len(modes) > 0:
#         print('modes', current_run.modes)
#         print('\nMode objects loaded.\n')
#     # Run
#     current_run()
#     print('=====  Simulation Ended  =====')
#     print('\nSee you!')
#     quit()

# '''
# Normal mode
# '''

# while True:
#     cmd = input('>>> ').lower()
#     if cmd == 'setting':
#         N, T, alpha, beta, gamma, phi, delta, phi_V, phi_T, immune_time, verbose_mode = setting(N, T, alpha, beta, gamma, phi, delta, phi_V, phi_T, immune_time, verbose_mode)
#         population = Person.make_population(N)
#     elif cmd == 'other setting':
#         print('Leave blank if not changing the value(s).')
#         N, T, alpha, beta, gamma, phi, delta, phi_V, phi_T, immune_time, verbose_mode = setting_other(N, T, alpha, beta, gamma, phi, delta, phi_V, phi_T, immune_time, verbose_mode)
#     elif cmd == 'summary':
#         summary()
#     elif cmd == 'help':
#         help()
#     elif cmd == 'start' or cmd == 'run':
#         print('===== Simulation Running =====')
#         current_run = Simulation(population, T, population, alpha, beta, gamma, phi, delta, filename, immune_time, verbose_mode)
#         # Load modes
#         current_run.load_modes(modes)
#         if len(modes) > 0:
#             print('\nMode objects loaded.\n')
#         # Run
#         current_run()
#         print('=====  Simulation Ended  =====')
#     elif cmd == 'mode':
#         modes = set_mode(modes)
#     elif cmd == 'quit' or cmd == 'q':
#         print('See you!')
#         quit()
#     else:
#         print('Invalid input. Please check your command again.')
#         cmd = input('Commands [y/n]')
#         if cmd == 'y':
#             usage()
#     print('')








# def start(N,T,alpha,beta,gamma,phi,delta,mode_flag):
def start(N,T,alpha,beta,gamma,phi,delta):
    '''
    Set initial variables
    '''
    immune_time = 70

    verbose_mode = False  # Need to put here for initiating other objects (nwk and person if needed).
    population = Person.make_population(N)
    filename = ''  # Default file name to export (.csv). Change when use prompt 'export' cmd.

    # All objects should add into mode_master_list
    mode01 = mode.Mode01(population)
    mode10 = mode.Mode10(population, phi, beta)
    mode11 = mode.Mode11(population)

    mode_master_list = [mode01, mode10, mode11]


    modes = {}

    current_run = Simulation(population, T, population, alpha, beta, gamma, phi, delta, filename, immune_time, verbose_mode)
    # Load modes
    current_run.load_modes(modes)
    if len(modes) > 0:
        print('modes', current_run.modes)
        print('\nMode objects loaded.\n')
    # Run
    (x,y,z,w) = current_run()
    return (x,y,z,w)
    # quit()
