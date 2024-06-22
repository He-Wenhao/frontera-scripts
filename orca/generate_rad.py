
from ase.io.trajectory import Trajectory
from ase import io;
import os;
import fnmatch
import textwrap

NPAR = 6;

def write(filename, atoms, type_calc):
    dic = {1:'H', 6:'C',8:'O'};
    def write_pos(_charge,_multiplicity):
        file.write('* xyz {} {}\n'.format(_charge,_multiplicity))
        pos = atoms.get_positions();
        atm = atoms.get_atomic_numbers();
        n = len(pos);
        for i in range(n):
            file.write(dic[atm[i]]+'\t');
            for j in range(3):
                file.write(str(pos[i][j])+'\t');
            file.write('\n');
        file.write('*');
    if(type_calc == 'DLPNO-pvtz'):
        with open(filename,'w') as file:
            file.write(textwrap.dedent('''\
                ! DLPNO-CCSD(T) cc-pVTZ cc-pVTZ/C RIJCOSX def2/J TIGHTSCF
                %maxcore 12000
                %pal
                nprocs 10
                end
                ! LargePrint KeepDens
                %MDCI
                triples 1
                END
                %ELPROP
                dipole true
                quadrupole true
                END
                % OUTPUT
                Print[ P_Density ] 1        # converged density
                Print[ P_KinEn ] 1          # kinetic energy matrix
                END
            '''))
            write_pos(_charge=0,_multiplicity=2)        
    elif(type_calc =='B3LYP-pvdz'):
        with open(filename,'w') as file:
            file.write(textwrap.dedent('''\
                !B3LYP DEF2-SVP
                ! LargePrint PrintBasis KeepDens
                %maxcore 12000
                % OUTPUT
                Print[ P_Overlap ] 1        # overlap matrix
                Print[ P_Iter_F ] 1         # Fock matrix, for every iteration
                END
            '''))
            write_pos(_charge=0,_multiplicity=2)
    elif(type_calc =='B3LYP-pvdz-parallel'):
        with open(filename,'w') as file:
            file.write(textwrap.dedent('''\
                !B3LYP DEF2-SVP
                ! LargePrint PrintBasis KeepDens
                %maxcore 12000
                %pal
                nprocs 10
                end
                % OUTPUT
                Print[ P_Overlap ] 1        # overlap matrix
                Print[ P_Iter_F ] 1         # Fock matrix, for every iteration
                END
            '''))
            write_pos(_charge=0,_multiplicity=2)
    elif(type_calc =='ROHF-pvdz'):
        with open(filename,'w') as file:
            file.write(textwrap.dedent('''\
                ! ROHF cc-pVDZ 
                ! LargePrint PrintBasis KeepDens
                % shark
                usegeneralcontraction false
                partialgcflag 0
                end
                % maxcore 3000
                % OUTPUT
                Print[ P_Overlap ] 1        # overlap matrix
                Print[ P_Iter_F ] 1         # Fock matrix, for every iteration
                END
            '''))
            write_pos(_charge=0,_multiplicity=2)
    elif(type_calc =='noiter-pvdz'):
        with open(filename,'w') as file:
            file.write(textwrap.dedent('''\
                ! HF cc-pVDZ noiter
                ! LargePrint PrintBasis KeepDens
                % maxcore 3000
                % OUTPUT
                Print[ P_Overlap ] 1        # overlap matrix
                Print[ P_Iter_F ] 1         # Fock matrix, for every iteration
                END
            '''))
            write_pos(_charge=0,_multiplicity=2)



route = os.getcwd();
#traj = Trajectory(route+'/data.traj');
#os.mkdir('pvdz');
#os.mkdir('pvtz');

#generate for each radicals
#get all radical data files
def find_files(directory, pattern):
    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches

# Use the function to find files
pattern = 'data_radical*.traj'
directory = '.'  # Current directory, change this as needed
files = find_files(directory, pattern)
folder_names = [raw_file[14:-5] for raw_file in files]
print('dbg',folder_names)
for raw_file in files:
    file = str(raw_file[1:])
    print(file)
    type_dict = {'B3LYP-pvdz':'B3LYP-pvdz-parallel'}
    for folder in ['B3LYP-pvdz']:
        #os.makedirs(route+file[:-5]+'/pvdz', exist_ok=True)
        #os.makedirs(route+file[:-5]+'/pvtz', exist_ok=True)
        

        i_index = 0;
        
        for atoms in Trajectory(route+file):
            dir_path = route+'/'+file[13:-5]+'/'+folder+'/'+str(i_index)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True);

            write(route+'/'+file[13:-5]+'/'+folder+'/'+str(i_index)+'/run.inp',atoms,type_dict[folder]);
            #print(route+'/'+file[13:-5]+'/'+folder+'/'+str(i_index)+'/run.inp')
        
            i_index += 1;
        
        