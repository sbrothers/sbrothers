import pandas as pd
import numpy as np
import argparse

class InputManager:
    
    def __init__(self):
        self.extension = '.json'
     
    def gen_new_key(self, data):
        key_table = []
        for key in data.keys():
            new_key = key.split('_')[0] + '_' + Input_structure[key.split('_')[1]] + '_' + key.split('_')[1]
            key_table.append(new_key)
        return key_table
    
    def gen_new_data(self, data):
        new_data = dict(zip(self.gen_new_key(data), data.values())) 
        return new_data
    
    def write_json(self, data, name):
        name = name + self.extension 
        data.to_json((name), orient='table')
            
    def read_json(self, name):
        name = name + self.extension
        return pd.read_json(name, orient='table')
    
    def num_str(self, data):
        return ['%.1e'% num for num in data]
    
    def splitting(self, pname, bname):
        df = self.read_json(pname)
        data = df.loc[0]
        df = df.drop(index=0)
        self.write_json(df, pname)
        self.write_json(data, bname)
        
    def read_inp(self, inp):
        name = inp + '.inp'
        with open(name, 'r') as f:
            lines = f.readlines()
        return lines
    
    def write_inp(self, inp, lines):
        name = inp + '.inp'
        with open(name, 'w') as f:
            f.writelines(lines)

    def parsing(self, json):
        data = []
        df = self.read_json(json)
        for index, value in zip(df.index, df.values):
            num, load, param = index.split('_')
            val = value[0]
            data.append([num, load, param, val])
        return data
    
    def navigate(self, param, inp):
        lines = self.read_inp(inp)
        line_indicator = []
        for i, line in enumerate(lines):
            if param in line:
                line_indicator.append(i)
        return line_indicator
    
    def modify_inp(self, json, inp, param):
        datas = self.parsing(json)
        line_index = self.navigate(param, inp)
        new_data = []
        i = 0
        for data in datas:
            if param in data:
                new_data.append([line_index[i], data[3]])
                i+=1
        lines = self.read_inp(inp)
        for data in new_data:
            new_line = param + '=' + data[1] + '\n'
            lines[data[0]] = new_line
        self.write_inp(inp, lines)

def main():
    parser = argparse.ArgumentParser(description='This code is written for automatic input txt modification')
    parser.add_argument('parameters', 
                        type=list,
                        metavar='parameters',
                        help='What parameters are you willing to use?')
    parser.add_argument('range', 
                        type=list,
                        metavar='value range',
                        help='What is the value range?')
    parser.add_argument('--op', 
                        type=str,
                        default='modify',
                        choices=['modify', 'generate'],
                        help='What operation?')
    
    args = parser.parse_args()
    params = args.parameters
    val_range = args.range
    append_val_range = []
    for i in range(len(params)):
        append_val_range.append(val_range)
        
    f = InputManager()
    var = f.num_str(val_range)
    data = dict([params, append_val_range])
    print(data)
    
if __name__ == "__main__":
    main()