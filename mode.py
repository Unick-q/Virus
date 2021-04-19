from person import Person

import random
import math

class Mode:
    def __init__(self, people, code):
        self.code = code
        # Flag to alert setting has been loaded.
        self.flag = ' '   # If loaded then has value 'X'.
        # Population objects
        self.people = people

    def raise_flag(self):
        '''
        If loaded then has value 'X'.
        '''
        self.flag = 'X'

    def drop_flag(self):
        '''
        If settings unloaded then mute the flagged icon.
        '''
        self.flag = ' '

    def correct_para(self, p, pos=False):
        '''
        Convert the parameters into integers.

        Parameters
        p: int
            input.
        pos: boolean
            If the parameter is positive number.
        '''
        try:
            p_num = int(p)
            if pos == True and p_num < 1:
                p_num = 1
            return p_num
        except ValueError:
            p_num = 1
            return p_num

    def set_correct_para(self, p, P, pos=False):
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
            return self.correct_para(p, pos=False)

    def correct_epi_para(self, p):
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

    def set_correct_epi_para(self, p, P):
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
            return self.correct_epi_para(p)

'''
=======================================================

Individual mode settings

=======================================================
'''


'''
01: Living in city/ rural
'''
class Mode01(Mode):
    '''
    Attributes
    ----------
    weight: {city, rural}
        Proportion of residents in city and rural respectively.
    betas: {city, rural}
        The infection rate while living in city or rural environment.
    '''

    def __init__(self, people, betas=[0.5,0.5]):
        super().__init__(people,1)
        self.weight = [4,6]
        self.betas = betas

    def set_weight(self, c, r):
        self.weight = [c,r]
        self.check_weight_integrity()

    def check_weight_integrity(self):
        if sum(self.weight) > 1:
            print('Warning: Weights too much. Set uniform proportion for city and suburban proportion. ')
            self.weight[0] = self.weight[1] = 5
        elif sum(self.weight) < 1:
            print('Warning: Weights too less. Proportion of rural residents is set to complement of city proportion. ')
            self.weight[1] = 1 - self.weight[0]

    def assign_regions(self):
        for person in self.people:
            person.location = random.choices(list(range(2)), weights = self.weight, k=1)[0]

    def __call__(self):
        '''
        When mode 1 is created.
        '''
        beta_city, beta_rural = self.betas[0], self.betas[1]
        prop_city, prop_rural = self.weight[0], self.weight[1]

        print('-------------------------')
        print('You are creating mode 1. ')
        print('-------------------------\n')
        print('Please set infection parameter below. ')
        beta_city_temp = input('City >>> ')
        beta_city = super().set_correct_epi_para(beta_city_temp, beta_city)
        self.set_beta(0, beta_city)
        beta_rural_temp = input('Rural >>> ')
        beta_rural = super().set_correct_epi_para(beta_rural_temp, beta_rural)
        self.set_beta(1, beta_rural)

        print('\nPlease set proportional parameter below. ')
        prop_city_temp = input('City >>> ')
        prop_city = super().set_correct_epi_para(prop_city_temp, prop_city)
        prop_rural_temp = input('Rural >>> ')
        prop_rural = super().set_correct_epi_para(prop_rural_temp, prop_rural)
        prop_city, prop_rural = self.weight[0], self.weight[1]
        print('{}: {}, {}: {}'.format(self.betas[0], self.betas[1], self.weight[0], self.weight[1]))
        print('We are assigning the population to regions.')
        self.assign_regions()
        self.raise_flag()
        print('\nMode 1 equipped. \n')

    def set_beta(self, idx, value):
        '''
        Set infection rate for each region.

        Arguments
        ---------
        idx: int
            The index according to Mode01.betas.
        '''
        self.betas[idx] = value


    def infect_01(self, idx, p):
        '''
        Model different infection rate due to residence.
        '''
        if self.people[idx].location == 0 and p < self.betas[0]:
            self.people[idx].suceptible = 1
        elif self.people[idx].location == 1 and p < self.betas[1]:
            self.people[idx].suceptible = 1

'''
10: Type of vaccine (One-off/ Seasonal/ Chemoprophylaxis)
'''
class Mode10(Mode):
    def __init__(self, people, phi, beta):
        super().__init__(people,10)
        self.types = ['One-off', 'Seasonal', 'Chemoprophylaxis']
        self.type = None

    def __call__(self):
        print('-------------------------')
        print('You are creating mode 10. ')
        print('-------------------------\n')
        print('Please set infection parameter below. ')
        for i in range(len(self.types)):
            print(f'{i+1}. {self.types[i]}')
        cmd = input('Please choose one option: ')
        if cmd == '1':
            self.type = 1
        elif cmd == '2':
            self.type = 2
        elif cmd == '3':
            self.type = 3
        self.raise_flag()
        print('\nMode 10 equipped. \n')

    def check_input(self, cmd):
        '''
        Check from express mode if user has input an integer the corresponds to an existing mode.
        '''
        try:
            cmd = int(cmd)
            if cmd > 0 and cmd <= 3:
                return cmd
        except ValueError:
            print('Invalid vaccine type specified. ')
'''
11: Initial infection by degree
'''
class Mode11(Mode):
    def __init__(self, people):
        super().__init__(people,11)
        self.init_infection = 5

    def __call__(self):
        '''
        Setting mode 11 into model.
        '''
        print('-------------------------')
        print('You are creating mode 11. ')
        print('-------------------------\n')
        print('Please set initial infection number below. ')
        Ii_temp = input('>>> ')
        self.init_infection = super().set_correct_para(Ii_temp, self.init_infection)
        self.raise_flag()
        print('\nMode 11 equipped. \n')

    def set_init_infection (self, Ii):
        return self.correct_para(Ii, pos=True)

