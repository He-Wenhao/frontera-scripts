import os;
import numpy as np;
import json;
from ase.io.cube import read_cube_data;
import scipy;

# Function to check if "TOTAL RUN TIME:" is in the log file
def check_total_run_time_exists(log_file_path):
    try:
        with open(log_file_path, 'r') as file:
            for line in file:
                if "TOTAL RUN TIME:" in line:
                    return True
        return False
    except FileNotFoundError:
        # Log file does not exist, thus returning False
        return False

Nframe = 10
os.chdir('pvtz')
rad_folder_list = [int(d) for d in os.listdir('.') if os.path.isdir(d)]
rad_folder_list.sort()
for rad_f in rad_folder_list:
    print('check done:',int(rad_f))
    if not check_total_run_time_exists(str(rad_f)+'/log'):
        Nframe = int(rad_f)
        break
os.chdir('..')

i_list = range(Nframe)

print('length =',len(i_list))

Elist = [];
posl  = [];
atm   = [];
nr = [];
grid = [];

E_orb = [];
E_nn = [];
E_HF = [];

route = os.getcwd()+'/';
u = -2;
while(route[u]!='/'):
    u -= 1;
u_tmp = u-1
while(route[u_tmp]!='/'):
    u_tmp -= 1;
name = route[u_tmp+1:u]+'_'+route[u+1:-6]+'_'+route[-6:-1];

res = os.popen("grep 'Number of Electrons' pvdz/0/log").readline();
ne = float(res.split()[-1]);
print(ne)

os.chdir(route+'pvtz/');
for i,ind in enumerate(i_list): 
    print('folder:',i);
    res = os.popen("grep 'E(CCSD(T))' "+str(ind)+'/log').readline();
    if(len(res)!=0):
        E1 = float(res.split()[-1][:-1]);
    else:
        E1 = False;
    Elist.append(E1);
   
    res = os.popen("grep 'SINGLE POINT ENERGY' ../pvdz/"+str(i)+'/log').readline();
    if(len(res)!=0):
        E1 = float(res.split()[-1][:-1]);
    else:
        E1 = False;
    E_HF.append(E1);

    
    res = os.popen("grep 'One Electron Energy' ../pvdz/"+str(i)+'/log').readline();
    E_orb.append(float(res.split()[-4]));
    res = os.popen("grep 'Nuclear Repulsion' ../pvdz/"+str(i)+'/log').readline();
    E_nn.append(float(res.split()[-2]));

    
    posl.append([]);
    atm.append([]);
    with open(str(i)+'/run.inp','r') as file:
        data = file.readlines();
        n,test = 0,'';
        while(test != '* xyz'):
            n += 1;
            test = data[-n-2][:5];
        data = data[-1-n:-1];
        for dp in data:
            posl[-1].append([float(u[:-1]) for u in dp.split()[1:]]);
            atm[-1].append(dp.split()[0]); 
                       
    if('run.eldens.cube' in os.listdir(str(i))):
        data, atoms = read_cube_data(str(i)+'/run.eldens.cube');
        data = data[20:80,20:80,20:80].tolist();
        with open(str(i)+'/run.eldens.cube','r') as file:
            res = file.readlines();
            init = [float(x) for x in res[2].split()[1:]];
            dist = [float(res[3].split()[1]), float(res[4].split()[2]), float(res[5].split()[3])];
            init = [init[i]+dist[i]*20 for i in range(3)];
            grid.append([init,dist]);
            nr.append(data)
    else:
        nr.append(False);
        grid.append(False);

def readmat(data):
    number = int(data[-1].split()[0])+1;
    rep = int(round(len(data)/(number+1)));

    matl = [];
    for i in range(rep):
        res = [[float(t) for t in s.split()[1:]] for s in data[i*(number+1)+1:i*(number+1)+number+1]];
        matl.append(np.array(res));
        
    mat = np.hstack(matl)
    return mat;

m0list = [];
m1list = [];
slist = [];
os.chdir(route);

for i,ind in enumerate(i_list): 
    print(i)
    with open('pvdz/' + str(ind)+'/log', 'r') as file:
        output =  file.readlines();
        u =  0;
        check_convergence = False
        for up in output:
            if '**** Energy Check signals convergence ****' in up or '***DIIS convergence achieved***' in up:
                check_convergence = True
        if check_convergence:
            while('signals convergence' not in output[u] and '***DIIS convergence achieved***' not in output[u]):
                u += 1;
                if('OVERLAP MATRIX' in output[u]):
                    s = int(u)+1;
                if('INITIAL GUESS: MOREAD' in output[u]):
                    t = int(u)-1;
                if('INITIAL GUESS: MODEL' in output[u]):
                    t = int(u)-3;
            v = int(u);
            while('Fock matrix for operator 1' not in output[v]):
                v -= 1;
            v_mat1 = v
            while('Fock matrix for operator 0' not in output[v]):
                v -= 1;
            v_mat0 = v
            
            dataf0 = output[v_mat0+1:v_mat1];
            dataf1 = output[v_mat1+1:u];

            dataS = output[s+1:t];
        else:
            while('WARNING: the maximum gradient error' not in output[u]):
                u += 1;
                if('OVERLAP MATRIX' in output[u]):
                    s = int(u)+1;
                if('INITIAL GUESS: MOREAD' in output[u]):
                    t = int(u)-1;
                if('INITIAL GUESS: MODEL' in output[u]):
                    t = int(u)-3;
            v = int(u);
            while('Fock matrix for operator 1' not in output[v]):
                v -= 1;
            v_mat1 = v
            while('Fock matrix for operator 0' not in output[v]):
                v -= 1;
            v_mat0 = v
            

            
            dataf0 = output[v_mat0+1:v_mat1];
            dataf1 = output[v_mat1+1:u-1];
            dataS = output[s+1:t];

    h0 = readmat(dataf0);
    #print(dataf0);
    h1 = readmat(dataf1);
    #print(dataf1);
    S = readmat(dataS);
#    S = scipy.linalg.fractional_matrix_power(S,-1/2);

    # stack together
    eigen_vals = np.hstack([scipy.linalg.eigvalsh(h1,S),scipy.linalg.eigvalsh(h0,S)])
    eigen_vals = np.sort(eigen_vals)

    delta_h = (-np.sum(eigen_vals[:int(ne+0.01)]) + E_HF[i] - E_nn[i])/ne*S;
    h1 += delta_h;
    h0 += delta_h;

    slist.append(S.tolist());
    m0list.append(h0.tolist());
    m1list.append(h1.tolist());

#integrator = integrate('cpu');
#Nik = [];
Sik = [];

#for i in range(int(Nframe//10)):
#    Nik += integrator.calc_N(posl[10*i:10*i+10],atm[10*i:10*i+10],nr[10*i:10*i+10],grid[10*i:10*i+10]).tolist();

output = {'coordinates':posl, 'HF': E_HF, 'elements':atm, 'S':slist, 'h0':m0list,'h1':m1list, 'energy':Elist, 'Enn':E_nn};
#print(output)

with open(name+'_data.json','w') as file:
    json.dump(output, file);

