from person import Person
from epidemic import Epidemic
# from contact import ContactNwk
import random

class Simulation:
    def __init__(self, N, T, people, alpha, beta, gamma, phi, delta, filename, immune_time, verbose_mode):
        self.N = N
        self.people = people   # List of people objects
        self.groups = None
        self.T = T

        # Adoption rate
        self.alpha = alpha

        # Infection rate
        self.beta = beta

        # Recovery rate
        self.gamma = gamma
        self.immune_time = immune_time

        # Wear off rate
        self.phi = phi

        # Removal rate
        self.delta = delta

        # Auxillary parameters
        self.verbose_mode = verbose_mode
        self.filename = filename
        self.modes = {}


    def load_modes(self,modes):
        '''Load mode objects into epidemic class, as defined in the main code.

        parameters
        ----------

        modes - dict:
            Keys are integer mode code with the corresponding mode objects
        '''
        self.modes = modes

    def __call__(self, modes=None, start=True):
        suspected = []
        infected = []
        vaccinated = []
        dead = []
        epidemic = Epidemic(self.alpha, self.beta, self.gamma, self.phi, self.delta, self.people, self.immune_time, self.verbose_mode, self.modes, self.filename, start)
        # epidemic.get_states()

        for t in range(self.T):
            print('=========== t = {} ============\n'.format(t+1))
            print('N = {}'.format(len(self.people)))
            print('S = {}, I = {}, V = {}, D = {}'.format(epidemic.S, epidemic.I, epidemic.V, epidemic.R))
            suspected.append(epidemic.S)
            infected.append(epidemic.I)
            vaccinated.append(epidemic.V)
            dead.append(epidemic.R)

        print('=========== Result =========\n')
        print('There are {} people infected.'.format(epidemic.I))
        print('There are {} people vaccinated.'.format(epidemic.V))
        print()
        return (suspected, infected, vaccinated, dead)
        # Return any data

