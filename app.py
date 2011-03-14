__author__ = 'samshe'

import os
import shutil
from subprocess import call

class ConsoleOption():
    def __init__(self, choice, title = '', method = ''):
        self.choice = choice
        self.title = title
        self.method = method

    def fire(self):
        consoleMethods = ConsoleMethods()
        consoleMethods.methods[self.method]()

class ConsoleMethods():
    def __init__(self):
        self.methods = {
            'hello': self.hello,
            'exit': self.exit,
            'apachesite': self.apachesite
        }

    def hello(self):
        print 'Hello World'

    def exit(self):
        exit()

    def apachesite(self):

        dir_available = '/etc/apache2/sites-available'
        dir_enabled = '/etc/apache2/sites-enabled'

        sites_available = os.listdir(dir_available)
        sites_enabled = os.listdir(dir_enabled)

        # Git a lit of options
        print 'Please choose an available site:'
        options = list()
        options_index = 0
        for site in sites_available:
            options_index += 1
            consoleOption = ConsoleOption(options_index, site)
            consoleOption.path = dir_available + '/' + site
            options.append(consoleOption)
            print str(options_index) + ') ' + site

        # Captures selection
        option_selected = None
        input = getInput()
        if input == '':
            input = -1
        for option in options:
            if option.choice == int(input):
                option_selected = option
                break

        if option_selected is None:
            return

        # Clears enabled folder
        for site in sites_enabled:
            os.remove(dir_enabled + '/' + site)

        # Add the selected site.
        shutil.copyfile(option_selected.path, dir_enabled + '/' + option_selected.title)

        #        call('/etc/init.d/apache2 reload', shell=True)
        call('apache2ctl restart', shell=True)

class Main():
    options = list()

    def __init__(self):
        self.options.append(ConsoleOption(1, 'Change Apache Site', 'apachesite'))
        self.options.append(ConsoleOption(2, 'SayHello', 'hello'))
        self.options.append(ConsoleOption(0, 'Exit', 'exit'))

        while True:
            self.printMenu()
            input = getInput()
            if input == '':
                input = -1
            for option in self.options:
                if option.choice == int(input):
                    option.fire()
                    break

    def printMenu(self):
        call('clear', shell=True)
        print ''
        print 'Options'
        for option in self.options:
            print  str(option.choice) + ') ' + option.title


def getInput(message = '>> '):
    return raw_input(message)


main = Main()