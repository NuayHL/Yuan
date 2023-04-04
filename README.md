# YUAN 
### An Advanced Experiment Platform

#### 1. Recorder: `Yuan`
```python
# An example
from Yuan import Yuan

class YourProcess(Yuan):
    def __init__(self):
        super(YourProcess, self).__init__()
        self.log_on(log_file_path='./log') # setting the main log path
        
    def process1(self):
        self.print('Starting Process1') # both shown in the console and log
        self.console_print('Begin...') # only print on the console
        self.log_info('Starting the pre processing....') # only record in the main log
        
    def process2(self, certain_condition):
        if certain_condition:
            self.silent() # you can silence a instance of this class by using is func
        self.error('unexpected output..') # throw a error warning both on recorder and console
            
    def process3(self, certain_condition):
        if certain_condition:
            self.log_on()
            self.console_on() # turn on the console output
```
`Yuan` used as base class acting as a log recorder or console printer
for any action you define.

Check the document for more usage in `Yuan`

#### 2. Simple File System: `FileManager`
```python
from Yuan import FileManager

experiement_path = './exp'
filesys = FileManager(experiement_path)
```
It use the relative file path to control the file func.

#### 3. `Register`
```python
import torch.nn as nn
from Yuan import Registry

backbone_registry = Registry('backbone')

@backbone_registry
@backbone_registry('net1')
class Net1(nn.Module):
    def __init__(self):
        ...

@backbone_registry
class Net2(nn.Module):
    def __init__(self):
        ...

my_net1 = backbone_registry['net1'] # get Net1 class
my_net2 = backbone_registry['Net2'] # get Net2 class

net = my_net1()
```

#### 4. Beautiful Progressbar: `IterProgressBar`, `ManualProgressBar`
```python
import time
from Yuan import IterProgressBar, ManualProgressBar

a = range(50)

a_bar = IterProgressBar(a, barlenth=40, prestr='example', endstr='counting...')
for i in a_bar:
    time.sleep(0.05)
    a_bar.update("i = %d" % i)

a_mbar = ManualProgressBar(a, barlenth=40, prestr='example', endstr='counting...')
for i in a:
    time.sleep(0.05)
    a_mbar.update("i = %d" % i)
```

#### 5. Colorful str output: `ColorStr`
```python
from Yuan import ColorStr as cs

print(cs.blue('This is a blue sentence'))
print(cs.red('This is a red sentence'))
```