# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 15:03:28 2024

@author: haota
"""

import os;
import numpy as np;
import multiprocessing as mp;
import json;
import shutil
from multiprocessing import Pool
import random
import json
import re


def delete_second_line(filename):
    # Read the contents of the file
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Modify the second line (index 1 in zero-indexed list)
    if len(lines) > 1:  # Check if there is a second line
        lines[1] = '\n'

    # Write the modified content back to the file
    with open(filename, 'w') as file:
        file.writelines(lines)


def convert_star_caret_to_decimal(filename):
    try:
        # Open the file and read its contents
        with open(filename, 'r') as file:
            content = file.read()
        
        # Define the function to replace the pattern with the calculated value
        def replace_function(match):
            a = float(match.group(1))
            b = int(match.group(2))
            return f'{a * (10 ** b):.10f}'  # Ensure decimal representation with 10 decimal places
        
        # Use regex to find patterns and replace them with calculated values
        modified_content = re.sub(r'([-+]?\d*\.?\d+)\*\^([-+]?\d+)', replace_function, content)
        
        # Save the modified contents back to the file or to a new file
        with open(filename, 'w') as file:
            file.write(modified_content)
        
        print("File has been updated successfully.")
    except FileNotFoundError:
        print("The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")




def float1(string):
        try:
            out = float(string);
        except:
            out = 0.;
        return out;

def write_orca_xyz(filename, xyzname ,type_calc):
    

    with open(filename,'w') as file:
        if(type_calc == 'pvtz_DLPNO_CCSD'):
        
            file.write('! DLPNO-CCSD cc-pVTZ cc-pVTZ/C RIJCOSX def2/J TIGHTSCF\n');
            file.write('%maxcore 12000\n');
            file.write('%pal\n');
            file.write('nprocs '+str(10)+'\n');
            file.write('end\n');
            file.write('! LargePrint KeepDens\n');
            file.write('%MDCI\n');
            file.write('maxiter 200\n');
            file.write('Density linearized\n');
            file.write('END\n');
    
            file.write('%ELPROP\n');
            file.write('  dipole true\n');
            file.write('  quadrupole true\n');
            file.write('END\n');
    
            file.write('% OUTPUT\n');
            file.write('  Print[ P_Density ] 1        # converged density\n');
            file.write('  Print[ P_KinEn ] 1          # kinetic energy matrix\n');
            file.write('END\n');
        if(type_calc == 'pvdz_DLPNO_CCSD'):
        
            file.write('! DLPNO-CCSD cc-pVDZ cc-pVDZ/C RIJCOSX def2/J TIGHTSCF\n');
            file.write('%maxcore 12000\n');
            file.write('%pal\n');
            file.write('nprocs '+str(10)+'\n');
            file.write('end\n');
            file.write('! LargePrint KeepDens\n');
            file.write('%MDCI\n');
            file.write('Density linearized\n');
            file.write('maxiter 200\n');
            file.write('END\n');
    
            file.write('%ELPROP\n');
            file.write('  dipole true\n');
            file.write('  quadrupole true\n');
            file.write('END\n');
    
            file.write('% OUTPUT\n');
            file.write('  Print[ P_Density ] 1        # converged density\n');
            file.write('  Print[ P_KinEn ] 1          # kinetic energy matrix\n');
            file.write('END\n');
        if(type_calc == 'pvtz_DLPNO_CCSDt'):
        
            file.write('! DLPNO-CCSD(T) cc-pVTZ cc-pVTZ/C RIJCOSX def2/J TIGHTSCF\n');
            file.write('%maxcore 12000\n');
            file.write('%pal\n');
            file.write('nprocs '+str(10)+'\n');
            file.write('end\n');
            file.write('! LargePrint KeepDens\n');
            file.write('%MDCI\n');
            file.write('maxiter 200\n');
            file.write('END\n');
    
            file.write('%ELPROP\n');
            file.write('  dipole true\n');
            file.write('  quadrupole true\n');
            file.write('END\n');
    
            file.write('% OUTPUT\n');
            file.write('  Print[ P_Density ] 1        # converged density\n');
            file.write('  Print[ P_KinEn ] 1          # kinetic energy matrix\n');
            file.write('END\n');
        if(type_calc == 'pvdz_DLPNO_CCSDt'):
        
            file.write('! DLPNO-CCSD(T) cc-pVDZ cc-pVDZ/C RIJCOSX def2/J TIGHTSCF\n');
            file.write('%maxcore 12000\n');
            file.write('%pal\n');
            file.write('nprocs '+str(10)+'\n');
            file.write('end\n');
            file.write('! LargePrint KeepDens\n');
            file.write('%MDCI\n');
            file.write('maxiter 200\n');
            file.write('END\n');
    
            file.write('%ELPROP\n');
            file.write('  dipole true\n');
            file.write('  quadrupole true\n');
            file.write('END\n');
    
            file.write('% OUTPUT\n');
            file.write('  Print[ P_Density ] 1        # converged density\n');
            file.write('  Print[ P_KinEn ] 1          # kinetic energy matrix\n');
            file.write('END\n');
        if(type_calc == 'pvtz_CCSDt'):
        
            file.write('! CCSD(T) cc-pVTZ\n');
            file.write('%maxcore 12000\n');
            file.write('%pal\n');
            file.write('nprocs '+str(10)+'\n');
            file.write('end\n');
            file.write('! LargePrint KeepDens\n');
            file.write('%MDCI\n');
            file.write('maxiter 200\n');
            file.write('END\n');
    
            file.write('%ELPROP\n');
            file.write('  dipole true\n');
            file.write('  quadrupole true\n');
            file.write('END\n');
    
            file.write('% OUTPUT\n');
            file.write('  Print[ P_Density ] 1        # converged density\n');
            file.write('  Print[ P_KinEn ] 1          # kinetic energy matrix\n');
            file.write('END\n');
        if(type_calc == 'pvdz_CCSDt'):
        
            file.write('! CCSD(T) cc-pVDZ\n');
            file.write('%maxcore 12000\n');
            file.write('%pal\n');
            file.write('nprocs '+str(10)+'\n');
            file.write('end\n');
            file.write('! LargePrint KeepDens\n');
            file.write('%MDCI\n');
            file.write('maxiter 200\n');
            file.write('END\n');
    
            file.write('%ELPROP\n');
            file.write('  dipole true\n');
            file.write('  quadrupole true\n');
            file.write('END\n');
    
            file.write('% OUTPUT\n');
            file.write('  Print[ P_Density ] 1        # converged density\n');
            file.write('  Print[ P_KinEn ] 1          # kinetic energy matrix\n');
            file.write('END\n');
        if(type_calc == 'bp86'):
        
            file.write('! BP86 def2-SVP\n');
            file.write('%maxcore 12000\n');
            file.write('%pal\n');
            file.write('nprocs '+str(10)+'\n');
            file.write('end\n');
    
    
            file.write('% OUTPUT\n');
            file.write('  Print[ P_Overlap ] 1        # converged density\n');
            file.write('  Print[ P_Iter_F ] 1          # kinetic energy matrix\n');
            file.write('END\n');
        if(type_calc == 'polar'):
        
            file.write('! CCSD cc-pVDZ\n');
            file.write('%maxcore 12000\n');
            file.write('%pal\n');
            file.write('nprocs '+str(10)+'\n');
            file.write('end\n');
            file.write('! LargePrint KeepDens\n');
            file.write('%MDCI\n');
            file.write('maxiter 200\n');
            file.write('END\n');
    
    
            file.write('%ELPROP\n');
            file.write('  polar 2    \n');
            file.write('END\n');
        if(type_calc == 'EOM'):
        
            file.write('! RHF EOM-CCSD cc-pVDZ TightSCF\n');
            file.write('%maxcore 12000\n');
            file.write('%pal\n');
            file.write('nprocs '+str(10)+'\n');
            file.write('end\n');
            file.write('! LargePrint KeepDens\n');
            file.write('%MDCI\n');
            file.write('nroots 3\n');
            file.write('END\n');
    


        file.write('* xyzfile 0 1 '+xyzname+'\n');     # * xyzfile 0 2 hydroxide.xyz

# we put every 1000 datas in a batch
def worker_rand(file_info):
    type_calc, path, file, ind = file_info
    batch_ind = ind // 1000
    name = os.path.join(path, str(batch_ind), str(ind%1000))
    task = os.path.join(name, type_calc)

    if not os.path.exists(name):
        os.makedirs(name, exist_ok=True)
    if not os.path.exists(task):
        os.makedirs(task, exist_ok=True)
    print('config:', file)

    write_orca_xyz(os.path.join(task, 'run.inp'), file, type_calc)
    shutil.copy(os.path.join('QM9', file), task)
    delete_second_line(os.path.join(task, file))
    convert_star_caret_to_decimal(os.path.join(task, file))

def make_all_orca_inp_rand(type_calc, path='orca'):
    # Open the JSON file in read mode
    with open('random_namelist.json', 'r') as file:
        # Load the list from the JSON file
        files = json.load(file)
    print('#file:',len(files))
    #files = files[0:3]
    if not os.path.exists(path):
        os.makedirs(path)

    # Create tuples of arguments to pass to the worker function
    file_info_l = []
    for ind, file in enumerate(files):
        file_info = (type_calc, path, file, ind)
        file_info_l.append(file_info)
    with Pool() as pool:
        # map the worker function to the files
        pool.map(worker_rand, file_info_l)

def randomize_namelist():
    files = os.listdir('QM9/')
    print(type(files))
    random.shuffle(files)
    random_files = files
    print(len(random_files))
    # Open a file in write mode
    with open('random_namelist.json', 'w') as file:
        # Write the list to the file in JSON format
        json.dump(random_files, file)

if __name__ == '__main__':
    #randomize_namelist()
    make_all_orca_inp_rand(type_calc = 'pvtz_DLPNO_CCSDt')
    make_all_orca_inp_rand(type_calc = 'pvdz_DLPNO_CCSDt')
    make_all_orca_inp_rand(type_calc = 'pvtz_DLPNO_CCSD')
    make_all_orca_inp_rand(type_calc = 'pvdz_DLPNO_CCSD')
    #make_all_orca_inp_rand(type_calc = 'pvdz_CCSDt')
    #make_all_orca_inp_rand(type_calc = 'EOM')
    #make_all_orca_inp_rand(type_calc = 'polar')
    #make_all_orca_inp_rand(type_calc = 'bp86')
