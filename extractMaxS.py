from odbAccess import *
from abaqusConstants import *
import sys, getopt, os, string
import math

def getPath(job_id):
    odbPath = job_id + '.odb'
    new_odbPath = None
    print odbPath
    if isUpgradeRequiredForOdb(upgradeRequiredOdbPath=odbPath):
        print "Upgrade required"
        path,file = os.path.split(odbPath)
        file = 'upgraded_'+file
        new_odbPath = os.path.join(path,file)
        upgradeOdb(existingOdbPath=odbPath, upgradedOdbPath=new_odbPath)
        odbPath = new_odbPath
    else:
        print "Upgrade not required"
    return odbPath

def Nf(Smax, R):
    '''
    Calculate Nf for Inconel 625, room temperature
    '''
    log_Nf = 24.49 - 9.62*math.log10(Smax*pow((1-R),0.42))
    N = math.pow(10, log_Nf)
    return N

def life_at_f(f, Smax, T, R):
    n_1sigma = 0.6827*f*T
    N_1sigma = Nf(Smax, R)
    n_2sigma = 0.2718*f*T
    N_2sigma = Nf(2*Smax, R)
    n_3sigma = 0.0428*f*T
    N_3sigma = Nf(3*Smax, R)
    life = n_1sigma/N_1sigma + n_2sigma/N_2sigma + n_3sigma/N_3sigma
    return life
    
def calc_accumulated_damage(max_values, T, R):
    sum = 0.0
    for f, Smax in max_values:
        sum = sum + life_at_f(f, Smax, T, R)
    return sum
        
def odbMaxStress(job_id):

    odbPath = getPath(job_id)
    odb = openOdb(path=odbPath)
    
    MaxValues = {}
    for instance_name in odb.rootAssembly.instances.keys():
        MaxValues[instance_name] = []

    # retrieve steps from the odb
    keys = odb.steps.keys()
    for key in keys:
        print key
        step = odb.steps[key]
        
        frames = step.frames

        for i in range(len(frames)):
        #for i in range(0,3):
            frame = frames[i]
            print 'Id = %d, Frequency = %f\n'%(frame.frameId,frame.frameValue)
            freq = frame.frameValue
            try:
                stress = frame.fieldOutputs['S']
                for val in MaxValues.itervalues():
                    val.append((freq, -1.0e20))
        
                # Doesn't make too much sense to use an invariant on the stress in a RR analysis, but I need something
                for stressValue in stress.values:
                    MaxValues[stressValue.instance.name][-1] = (freq, max(stressValue.mises, MaxValues[stressValue.instance.name][-1][1]))
                        
            except KeyError:
                print "fieldOutputs does not have RS at frame %s" % (frame.frameId,)
            
    odb.close()
    instances_to_delete = []
    def max_stress(a, b):
        if b[1] > a[1]:
            return b
        else:
            return a
    for instance_name, vals in MaxValues.iteritems():
        maximum = reduce(max_stress, vals)
        # Deleting the instances without any values.
        # Only true for a random response analysis, adjust to taste
        if maximum[1] < 0.0:
            instances_to_delete.append(instance_name)
    for instance_name in instances_to_delete:
        print "deleting %s" % (instance_name,)
        del MaxValues[instance_name]    
                        
    dest = job_id + "_MaxStress.txt"
    output = open(dest,"w")
    output.write( 'instance,f (Hz),S (ksi)\n')
    def convert_stress(s):
        if s > 0.0:
            return math.sqrt(val)/1000.0
        else:
            return 0.0001
    for instance_name, vals in sorted(MaxValues.iteritems()):
        # Convert to ksi, take square root
        vals = [(f, convert_stress(val)) for f, val in vals]
        for f, val in vals:
            output.write('%s,%f,%f\n' % (instance_name,f, val))
        T = 3600.0 # Duration of test in seconds
        R = -1 # Ration of max/min, -1 fully reversed
        output.write("Accumulated damage for instance %s: %s\n" % (instance_name, calc_accumulated_damage(vals, 3600.0, -1),))
    output.close()
        
if __name__ == '__main__':
        # Get command line arguments.
        
        usage = "usage: abaqus python <job name>"
        optlist, args = getopt.getopt(sys.argv[1:],'')
        JobID = args[0]
        if not JobID:
                print usage
                sys.exit(0)
        odbPath = JobID + '.odb'
        if not os.path.exists(odbPath):
                print "odb %s does not exist!" % odbPath
                sys.exit(0)
        excluded_instances = ['ASSY_6-1-1',]
        odbMaxStress(JobID)