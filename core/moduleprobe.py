

from moduleexception import ModuleException, ProbeException, ProbeSucceed
import types
from core.savedargparse import SavedArgumentParser as ArgumentParser, Namespace

class_name = 'Module'

class ModuleProbe:
    '''Generic class Module to inherit'''

    # self.args: variables related to current execution
    # self.stored_args: variables related to entire module life 

    def __init__(self, modhandler):
        

        self.modhandler = modhandler

        self.name = '.'.join(self.__module__.split('.')[-2:])
        
        self.__init_module_variables()
        self._init_module()

    def run(self, arglist = []):
        
        self._output = ''
        
        try:
            self._check_args(arglist)
            self._prepare_probe()
            self._probe()
            self._verify_probe()
        except ProbeException, e:
            self.mprint('[!] Error: %s' % (e.error), 2, e.module) 
        except ProbeSucceed, e:
            pass
        except ModuleException, e:
            module = self.name
            if e.module:
                module = e.module
            self.mprint('[!] Error: %s' % (e.error), 2, module) 
            
        return self._output

    def mprint(self, str, msg_class = 3, module_name = None):
        
        if not self.modhandler.verbosity or msg_class <= self.modhandler.verbosity[-1]:
            if not module_name:
                module_name = self.name
                
            print '[%s] %s' % (module_name, str)
            

    def _init_module(self):
        pass
    
    def __init_module_variables(self):
        self.stored_args = {}
    

    def _check_args(self, args):

        parsed_namespace, remaining_args = self.argparser.parse_known_stored_and_new_args(args=args, stored_args_dict = self.stored_args)
        self.args = vars(parsed_namespace)
        

    def _prepare_probe(self):
        pass
    
    def _verify_probe(self):
        pass    

    def _probe(self):
        pass

        
    def save_args(self, args):

        for argument in args:
            if '=' in argument:
                key, value = argument.split('=')
                
                # Reset value
                if value == '':
                    value = None
                
                self.stored_args[key] = value
        
                
    def print_saved_args(self):
    
        saved_args_str = ''
        for argument in [ action.dest for action in self.argparser._actions if action.dest != 'help' ]:
            value = self.stored_args[argument] if argument in self.stored_args else ''
            saved_args_str += '%s=\'%s\' ' % (argument, value)
        self.mprint(saved_args_str)
        
    