import angr
import sys

main_addr   = 0x4011a9
find_addr = 0x40135d
avoid_addr  = 0x40133c

class My_scanf(angr.SimProcedure):
    def run(self, fmt, n):
        simfd = self.state.posix.get_fd(sys.stdin.fileno())
        data, ret_size = simfd.read_data(4)
        self.state.memory.store(n, data)
        return 1

# Create Project
proj = angr.Project('./src/prog', load_options={'auto_load_libs': False})
proj.hook_symbol('__isoc99_scanf', My_scanf(), replace=True)

# Creat Initial State
state = proj.factory.blank_state(addr=main_addr)

# Create Simulation Manager
simgr = proj.factory.simulation_manager(state)

# Explore State 
simgr.explore(find=find_addr, avoid=avoid_addr)

# Dump the stdin of the state
if simgr.found:
    print(simgr.found[0].posix.dumps(sys.stdin.fileno()))
s = simgr.found[0].posix.dumps(sys.stdin.fileno())

d = []
for i in range(0, 15):
    d.append(int.from_bytes(s[i * 4 : i * 4 + 4], byteorder='little', signed=True))

for i in range(0,len(d)):
    print(d[i])
