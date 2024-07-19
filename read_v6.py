# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:02:56 2024

@author: haota
"""

import numpy as np;
from ase import io;
import os;
import shutil;
import json;
import scipy;
import multiprocessing
import pdb

class QM_reader(object):

    def __init__(self, route):

        self.route = route;

    def read_ne(self, folder):
       
        path  = self.route + folder + '/log';
        res = os.popen("grep 'Number of Electrons' " +path).readline();
        if res=='':
            print('dbg print:',path)
        ne = float(res.split()[-1]);
        print('N electrons:' + str(ne));
        self.ne = ne;
        return ne;

    def read_HF(self, folder):

        path  = self.route + folder + '/log';
        print('reading basic information: '+folder);

        res = os.popen("grep 'SINGLE POINT ENERGY' " + path).readline();
        if(len(res)!=0):
            E1 = float(res.split()[-1][:-1]);
        else:
            E1 = False;
        self.E_HF = E1;

        res = os.popen("grep 'Nuclear Repulsion' " + path).readline();
        self.E_nn = float(res.split()[-2]);

        self.posl = [];
        self.atm = [];
        name = [f1 for f1 in os.listdir(self.route + folder) if f1[-4:] == '.xyz'][0];
        with open(self.route + folder+'/'+ name,'r') as file:
            data = file.readlines();
            natoms = int(data[0]);
            for line in range(2, 2+natoms):
                dp = data[line];
                self.posl.append([float(u[:-1]) for u in dp.split()[1:4]]);
                self.atm.append(dp.split()[0]); 
        return {'HF': self.E_HF, 'coordinates': self.posl, 'elements': self.atm, 'Enn': self.E_nn};
    
    def readmat(self, data):
        number = int(data[-1].split()[0])+1;
        rep = int(round(len(data)/(number+1)));

        matl = [];
        for i in range(rep):
            res = [[float(t) for t in s.split()[1:]] for s in data[i*(number+1)+1:i*(number+1)+number+1]];
            matl.append(np.array(res));
            
        mat = np.hstack(matl)
        return mat;

    def read_matrix(self, folder):
        
        path  = self.route + folder + '/log';
        print('reading matrix information: '+folder);
        with open(path, 'r') as file:
            output =  file.readlines();
            u =  0;

            while('signals convergence' not in output[u]):
                u += 1;
                if u == len(output):
                    print('dbg path:',path)
                if('OVERLAP MATRIX' in output[u]):
                    s = int(u)+1;
                if('Time for model grid setup' in output[u]):
                    t = int(u);
            v = int(u);
            while('Fock matrix for operator 0' not in output[v]):
                v -= 1;
            dataf = output[v+1:u];
            dataS = output[s+1:t];

            h = self.readmat(dataf);
            S = self.readmat(dataS);

            h += (-np.sum(scipy.linalg.eigvalsh(h,S)[:int(self.ne/2)])*2 + self.E_HF - self.E_nn)/self.ne*S;

        return {'S': S.tolist(), 'h': h.tolist()};

    def read_ccsdt(self, folder):

        path  = folder + '/log';
        res = os.popen("grep 'E(CCSD(T))' "+ path).readline();
        try:
            E1 = float(res.split()[-1][:-1]);
        except:
            E1 = None;
        dipole = os.popen("grep 'Electronic contribution' " + path);
        dipole = [-float(u) for u in dipole.readlines()[-1].split()[-3:]];

        quadrupole = os.popen("grep EL " + path);
        quadrupole = [-float(u) for u in quadrupole.readlines()[-1].split()[-6:]];
        natom = len(self.atm);
        command = "grep -A "+str(natom+1)+" 'MULLIKEN ATOMIC CHARGE' ";
        atomicCharge = os.popen(command + path).readlines()[-natom:];
        atomicCharge = [float(u[:-1].split()[-1]) for u in atomicCharge];

        command = "grep -A "+str(20)+" 'Mayer bond orders' ";
        bond_data = os.popen(command + path).readlines();
        i_ind = -1;
        while('Mayer bond orders' not in bond_data[i_ind]):
            i_ind -= 1;
        i_ind += 1;
        bond_order = [];
        while('B' in bond_data[i_ind]):
            u = bond_data[i_ind][:-1].split();
            j_ind = 0;
            while(7*j_ind+7<=len(u)):
                bond_order.append([int(u[7*j_ind+1][:-2]),
                                   int(u[7*j_ind+3][:-2]),
                                   float(u[7*j_ind+6])
                                   ])
                j_ind += 1;
            i_ind += 1;

        return {'energy': E1, 
                'atomic_charge': atomicCharge, 'bond_order': bond_order,
                'x':dipole[0], 'y':dipole[1], 'z':dipole[2], 'xx':quadrupole[0],
                'yy':quadrupole[1], 'zz':quadrupole[2], 'xy':quadrupole[3],
                'xz':quadrupole[4], 'yz':quadrupole[5]};

    def read_obs(self, folder):
        
        path  = self.route + folder + '/';
        obs_dic = {};

        pvdz_ccsdt = self.read_ccsdt(path + 'pvdz_CCSDt');
        pvdz_dlpno_den = self.read_ccsdt(path + 'pvdz_DLPNO_CCSD');
        pvtz_dlpno_den = self.read_ccsdt(path + 'pvtz_DLPNO_CCSD');
        pvdz_dlpno_E = self.read_ccsdt(path + 'pvdz_DLPNO_CCSDt');
        pvtz_dlpno_E = self.read_ccsdt(path + 'pvtz_DLPNO_CCSDt');

        for key in pvdz_ccsdt:

            if(key == 'atomic_charge'):
                obs_dic[key] = (np.array(pvdz_ccsdt[key]) + np.array(pvtz_dlpno_den[key]) - np.array(pvdz_dlpno_den[key])).tolist();
            elif(key == 'bond_order'):
                output = [];
                d1 = [u[:2] for u in pvdz_dlpno_den[key]];
                d2 = [u[:2] for u in pvtz_dlpno_den[key]];
                for bond in pvdz_ccsdt[key]:
                    if(bond[:2] in d1):
                        b1 = pvdz_dlpno_den[key][d1.index(bond[:2])][2];
                    else: 
                        b1 = 0;
                    if(bond[:2] in d2):
                        b2 = pvtz_dlpno_den[key][d2.index(bond[:2])][2];
                    else: 
                        b2 = 0;
                    output.append(bond[:2] + [bond[2]-b1+b2]);
                obs_dic[key] = output;

            elif(key == 'energy'):
                obs_dic[key] = pvdz_ccsdt[key] + pvtz_dlpno_E[key] - pvdz_dlpno_E[key];
            else:
                obs_dic[key] = pvdz_ccsdt[key] + pvtz_dlpno_den[key] - pvdz_dlpno_den[key];

        res = os.popen("grep 'Nuclear Repulsion' "+ path +'bp86/log').readline();
        obs_dic['E_nn'] = float(res.split()[-2]);
        
        dp = os.popen("grep -A 7 'ABSORPTION SPECTRUM' "+ path +'EOM/log').readlines();
        dp = [[float(v) for v in u.split()] for u in dp[-3:]];
        obs_dic['Ee'] = [u[1] for u in dp];
        obs_dic['T'] = [[u[5],u[6],u[7]] for u in dp];
        
        dp = os.popen("grep -A 3 'The raw cartesian tensor' "+ path +"polar/log").readlines();
        dp = [[float(v) for v in u.split()] for u in dp[-3:]];
        obs_dic['alpha'] = dp;
        
        return obs_dic;

def worker(Nm): 
    #pdb.set_trace()   
    output = {};    
    path = read_dir + Nm + '/bp86/';
    ne = reader.read_ne(path);
    HF_dic = reader.read_HF(path);
    matrix_dic = reader.read_matrix(path);
    obs_dic = reader.read_obs(path[:-5]);

    for key in HF_dic:
        output[key] = HF_dic[key];
    for key in matrix_dic:
        output[key] = matrix_dic[key];

    labels = {};
    for key in obs_dic:
        labels[key] = obs_dic[key];
    output['name'] = Nm;
    labels['name'] = Nm;

    ele = HF_dic['elements'];
    N = [ele.count('H'), ele.count('C'), ele.count('N'), ele.count('O'),ele.count('F')];
    string = '';
    for u in N:
        string += str(u)+'_';
    with open(route+out1+'/'+Nm + '_' + string[:-1] + '.json','w') as file:
        json.dump(output, file);

    with open(route + out2 + '/'+Nm + '.json','w') as file:
        json.dump(labels, file);

read_dir = './';
parent_directory = os.path.basename(os.path.abspath(read_dir))
data_folder =  'orcaData'+str(parent_directory) 
out1 = data_folder + '/basic';
out2 = data_folder + '/obs';

Nl = os.listdir(read_dir);
Nl = [p for p in Nl if os.path.isdir(os.path.join(read_dir, p)) and p.isdigit()]
#Nl.remove('538')
if(not os.path.exists(data_folder)):
    os.mkdir(data_folder)
if(not os.path.exists(out1)):
    os.mkdir(out1)
if(not os.path.exists(out2)):
    os.mkdir(out2);

route = os.getcwd()+'/';
reader = QM_reader(route);



with multiprocessing.Pool(processes=50) as pool:
    pool.map(worker, Nl)

