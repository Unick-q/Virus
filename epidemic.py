import random
import numpy as np
import person

class Epidemic:

    def __init__ (self, vaccinated, infection, recover, resus, remove, people, immune_time, contact_nwk, verbose_mode, modes=None, start=True):
        '''Initial elements

        Attributes
        ----------

        epidemic - int
            Flag epidemic starts or ends.

        people - People
            Agents for simulation
        '''
        self.epidemic = 0   # Whether an epidemic occured or not.
        self.people = people
        self.contact_nwk = contact_nwk
        self.mode = {}  # Dict of modes loaded. Values are mode objects

        try:
            if vaccinated >= 0 and vaccinated <= 1:
                self.vaccinated = vaccinated   # Probability to get vaccinated
            else:
                raise ValueError
            if infection >= 0 and infection <= 1:
                self.infection = infection
            else:
                raise ValueError
            if recover >= 0 and recover <= 1:
                self.recover = recover  # Recovery rate
            else:
                raise ValueError
            if remove >= 0 and remove <= 1:
                self.remove = remove  # Recovery rate
            else:
                raise ValueError
            if resus >= 0 and resus <= 1:
                self.resus = resus
            else:
                raise ValueError

            self.immune_time = immune_time

            # Auxillary parameter
            self.verbose_mode = verbose_mode


            '''Compartment statics

            Number of agents within a compartment.

            Attributes
            ----------
            S: int
                Number of people not infected (susceptible).
            U: int
                Number of people with COVID-19 symptoms observed.
            E: int
                Number of people with COVID-19 symptoms observed, assumed quarantined.
            I: int
                Sum of people in E and U. Number of infected agents.
            V: int
                Number of people taken PrEP
            R: int
                Number of people removed.
            '''
            self.S = len(self.people)
            self.U = 0
            self.E = 0
            self.I = self.U + self.E
            self.V = 0
            self.R = 0

            if start == True:
                self.load_modes(modes)
                self.set_epidemic(1)


        except ValueError:
            print('Check your parameters if they are probabilities.')

    def get_states(self):
        '''
            Get number of people who are in S, I or V state.
        '''
        self.S = 0
        self.I = 0
        self.U = 0
        self.E = 0
        self.V = 0
        self.R = 0
        for i in range(len(self.people)):
            if self.people[i].vaccinated == 1:
                self.V += 1
                continue
            elif self.people[i].suceptible == 1 and self.people[i].removed == 0:
                self.U += 1
                continue
            elif self.people[i].exposed == 1 and self.people[i].removed == 0:
                self.E += 1
                continue
            elif self.people[i].removed == 1:
                self.R += 1
                continue
            self.S += 1
        self.I = self.U + self.E
        return self.S, self.I, self.U, self.E, self.V, self.R

    def set_epidemic(self, mode):
        '''
        Set either the environment to be disease-free or not.
        '''
        try:
            if mode > 1 or mode < 0:
                raise ValueError
        except ValueError:
            print('Mode must be either 1 or 0')
            pass
        if mode == 1:
            self.epidemic = 1
            if 11 in self.mode:
                Epidemic.start_epidemic(self, self.mode[11].init_infection)
            else:
                Epidemic.start_epidemic(self)
        else:
            self.epidemic = 0
            Epidemic.kill_epidemic(self)

    def start_epidemic(self, initial_infection=4):
        '''
        Start an epidemic
        '''
        if len(self.people) < initial_infection:
            initial_infection = len(self.people)
        # Pick first 4 people/ random number of people (defined by mode 11) infected initially
        # if 505 in self.mode:
        if 11 in self.mode:
            self.mode[505].set_infection(self.mode[11].init_infection)
            # else:
            #     self.mode[505].set_infection()
            return
        for i in range(initial_infection):
            self.people[i].suceptible = 1

    def kill_epidemic(self):
        for i in range(len(self.people)):
            self.people[i].suceptible = 0

    def load_modes(self, modes):
        self.mode.update(modes)

    def vaccinate(self):
        for i in range(len(self.people)):
            seed = random.randint(0,10000)/10000
            if 4 in self.mode:
                if self.verbose_mode == True:
                    print(self.mode[4].P_Alpha[i])
                if seed < self.mode[4].P_Alpha[i] and self.people[i].vaccinated == 0:
                    if self.verbose_mode == True:
                        print(f'{self.people[i].id} has decided to take vaccine. ')
                    self.people[i].vaccinated = 1
                continue
            if self.people[i].suceptible == 1:
                continue

            if seed < self.vaccinated and self.people[i].vaccinated == 0:
                if self.verbose_mode == True:
                    print(f'{self.people[i].id} has decided to take vaccine. ')
                self.people[i].vaccinated = 1

    def removed(self):
        '''
        A person is removed from population.
        '''
        for i in range(len(self.people)):
            if self.people[i].suceptible != 1:
                continue
            seed = random.randint(0,1000)/1000

            if seed < self.remove:
                self.people[i].removed = 1

    def infect(self):
        '''
        Mechanism of infection.
        '''

        beta_pp = np.ones(len(self.people))
        for i in range(len(self.people)):
            if any(i in self.mode for i in [1]):
                # Fetch all parameters:
                if 1 in self.mode:
                    beta_pp[i] = np.multiply(self.mode[1].betas[self.people[i].location], beta_pp[i])

        for i in range(len(self.people)):
            '''
            Infect (or not)
            '''
            if self.people[i].suceptible == 1:
                if self.verbose_mode == True:
                    print(f'{self.people[i].id} has already been infected and will not be infected. ')
                continue  # Skip
            if self.people[i].removed == 1 :
                if self.verbose_mode == True:
                    print(f'{self.people[i].id} is removed and will not be infected. ')
                continue  # Skip

            seed = random.randint(0,1000)/1000

            '''
            Normal infection event
            '''
            if seed < self.infection:
                if self.verbose_mode == True:
                    print(f'{self.people[i].id} is infected. ')
                self.people[i].suceptible = 1

    def infection_clock(self, i):
        if self.people[i].infection_clock > 14:
            self.people[i].exposed = 1

    def infected(self):
        '''
        Once a person was infected for 14 days, their symptoms are exposed.

        If the person is tested, we may put them into E compartment.
        '''
        for i in range(len(self.people)):
            if self.people[i].suceptible == 1 and self.people[i].removed == 0:
                self.people[i].infection_clock += 1
            else:
                self.people[i].infection_clock = 0

            self.infection_clock(i)

    def recovery(self):
        for i in range(len(self.people)):
            seed = random.randint(0,100000)/100000
            if 11 in self.mode:
                if seed < self.mode[11].gamma_V:
                    self.people[i].suceptible = 0
                    self.people[i].exposed = 0
            if seed < self.recover:
                self.people[i].suceptible = 0
                self.people[i].exposed = 0

    def immune(self):
        '''
        Assume there is a period of immunity since recovery.
        '''
        if self.immune_time == 0:
            return
        for i in range(len(self.people)):
            recent = self.people[i].compartment_history[-self.immune_time:]
            for j in range(len(recent)-1):
                if len(recent) < 2:
                    continue
                if recent[j] == 'I' and recent[j+1] == 'S':
                    self.people[i].suceptible = 0
                    self.people[i].exposed = 0
                    continue

    def wear_off(self):
        '''
        Vaccine may wear off.
        '''
        if 10 in self.mode:
            if self.mode[10].type == 1:
                return # Patients will not have their vaccine wear-off.
            elif self.mode[10].type == 2:
                for i in range(len(self.people)):
                    # See people are unlikely to leave V compartment.
                    recent = self.people[i].compartment_history[-366//4:]
                    for j in range(len(recent)-1):
                        if len(recent) < 2:
                            continue
                        if recent[j] == 'S' and recent[j+1] == 'V':
                            # Maintain V state and iterate to next person
                            self.people[i].vaccinated = 1
                            continue
                    # Else
                    seed = random.randint(0,100000)/100000
                    if self.people[i].vaccinated == 1 and seed <= self.resus:
                        self.people[i].vaccinated = 0
        for i in range(len(self.people)):
            seed = random.randint(0,100000)/100000
            if self.people[i].vaccinated == 1 and seed <= self.resus:
                self.people[i].vaccinated = 0

    def next(self):
        '''
        At each iteration, there will be:
        * Calculate S, I, V and proportion of pro and against vaccine.
        * Each person interacts with another.

        '''

        self.get_states()
        self.wear_off()
        self.infect()
        self.removed()
        self.recovery()
        self.vaccinate()
        self.infected()
        self.immune()