import numpy as np 
import json
import copy

#global lists track loaded and created nodes for error checking and easy saving
nodesSave = []
parentsSave = []
statesSave = []
cptsSave = []
cpts = []

def load (filepath):
    '''Load in existing notwork'''
    with open(filepath) as nodes:
        nodes = json.load(nodes)
        for x in range(0,len(nodes)):
            temp1 = ''.join(nodes[x]["Parents"])
            temp2 = temp1[::-1]
            together = temp2 + nodes[x]["Name"]
            cpt = nodes[x]["cpt"]
            cpts.append(TablePotential(together,cpt))
            #append for easy saving later
            nodesSave.append(nodes[x]["Name"])
            parentsSave.append(nodes[x]["Parents"])
            statesSave.append(nodes[x]["States"])
            cptsSave.append(nodes[x]["cpt"])


class TablePotential:
    '''Subsets user-supplied conditional probability tables based on evidence set (non-evidence is set to zero)'''
    def __init__(self, dim, table, index=None):
        if (index != None):
            self.table = np.zeros(table)
            self.table[index] = 1
        else:
            self.table = np.array(table)
            self.dim = dim
        self.dim = dim

def doInference(potentials):
    '''Return probabilities given evidence set by the user'''
    print("")
    dim = [i.dim for i in potentials]
    pots = [i.table for i in potentials]
    einsumFormat = ','.join(dim) 
    vars = sorted(list(set(''.join(dim)))) 

    for v in vars:
        vMarginal = np.einsum(einsumFormat+'->'+ v, *pots) 
        vMarginal = vMarginal / np.sum(vMarginal)
        print("{} -> {}".format(v,vMarginal))

    varsString = ''.join(vars)
    joint = np.einsum(einsumFormat+'->'+varsString,*pots)
    joint = joint/np.sum(joint)
    print("{} -> {}".format(varsString, joint))

def createNode():
    '''Create a node by inputting its name, parents, states, and distribution'''
    cProb = []
    name = input('Please enter name of new node (parent nodes must be created before their children): ')
    nodesSave.append(name) #add to global list
    numParents = int(input('Please enter the number of parents for new node (parent nodes must be created before children): '))
    assert isinstance (numParents, int) #assert integer
    states = []
    numStates = int(input('Please enter number of states for new node: '))
    assert isinstance(numStates, int) #assert integer
    for y in range(0,numStates):
        states.append(input('Please enter name for state ' + str(y+1) + ': '))
    statesSave.append(states) #add to global list
    if numParents > 0:
        parents = []
        for x in range(0,numParents):
            parents.append(input('Please enter name of parent ' + str(x+1) + ' in order that parent was entered: '))
        parentsCopy = copy.deepcopy(parents)
        parentsSave.append(parentsCopy)
        cProb = eval(input("Please enter conditional probability table with respect to the order that parents were entered: \n " + str(parents)))
        cptsSave.append(cProb) #add to global list
        parents.reverse() 
        parents = ''.join(parents)
        together = parents + name
    if numParents == 0: 
        cProb = eval(input("Please enter marginal probability table for node " + str(name) + ' in the form of a list: '))
        assert sum(cProb)==1, 'Marginal probabilities must add up to one.'
        cptsSave.append(cProb)
        together = name
        parentsSave.append([])
    cpt = TablePotential(together,cProb)
    cpts.append(cpt)
    return(cpt)

def getUserInput():
    '''Allow user to set evidence for created nodes'''
    evidenceList=[]
    nodeData=[]    
    evidenceNum=int(input('How many nodes do you have evidence for? ' )) 
    assert isinstance(evidenceNum, int), 'Input was not recognized.'  
    for i in range(0,evidenceNum):    
        print("")
        evidenceNode = input('Enter name of node %i: ' %(i+1))
        assert evidenceNode in nodesSave, 'Node not found.'
        evidenceNodeSize = int(input('Enter total number of states for this node: ' ))
        assert isinstance(evidenceNum, int), 'Input was not recognized.'
        nodeData.append(evidenceNodeSize)
        evidenceState = int(input('Which of these ' + '%i '%evidenceNodeSize + 'states ' +'for node %s'%evidenceNode + ' has evidence? Enter one number: ') )
        assert isinstance(evidenceNum, int), 'Input was not recognized. Must enter number.'
        nodeData.append(evidenceState)       
        evidence={evidenceNode:nodeData}
        evidenceList.append(evidence)
        nodeData=[]

    return evidenceList   
    
def setEvidenceList(evidenceList):
    '''Calls table potential function for supplied evidence'''
    setEvidences=[]
    for item in evidenceList:
        for key,value in item.items():
            currentStateEvidence=TablePotential(key,value[0],value[1]-1)        
        setEvidences.append(currentStateEvidence)
    return setEvidences

def deleteNode(node):
    cont = True
    for x in range(0,len(parentsSave)):
        if node in parentsSave[x]:
            print('This node cannot be deleted because it has child nodes that are dependent on it.\n Please delete child nodes of this node before deleting this node.')
            cont = False
    if cont == True:    
        index = nodesSave.index(node)
        del nodesSave[index]
        del parentsSave[index]
        del statesSave[index]
        del cptsSave[index]
        del cpts[index]

def save(filepath):
    with open(filepath, 'w') as outfile:
        network = []
        for z in range(0,len(nodesSave)):
            network.append({"Name": nodesSave[z],
                "Parents": parentsSave[z],
                "States": statesSave[z],
                "cpt": cptsSave[z]})
        json.dump(network, outfile)
    del nodesSave[:]
    del parentsSave[:]
    del statesSave[:]
    del cptsSave[:]
    del cpts[:]


#Test Case 
'''       
load("/users/kylehundman/desktop/input.json") #loads in z,x,a
# #must create nodes in this order (parent before its child). Also can't add nodes as parents of loaded nodes. Must work top to bottom.
createNode() #create c [ 0.1,  0.2,  0.3,  0.4]
createNode() #create b [[[ 0.2 ,  0.4 ,  0.4 ],[ 0.33,  0.33,  0.34]],[[ 0.1 ,  0.5 ,  0.4 ],[ 0.3 ,  0.1 ,  0.6 ]],[[ 0.01,  0.01,  0.98],[ 0.2 ,  0.7 ,  0.1 ]],[[ 0.2 ,  0.1 ,  0.7 ],[ 0.9 ,  0.05,  0.05]]]
createNode() #create e [[.1, .9],[.3,.7],[.6,.4]]
createNode() #create f [[.2, .8],[.55,.45]]
deleteNode('b') #won't work because it is a parent
#deleteNode('f') #will work because nothing is dependent on it
evidences = getUserInput()
doInference(cpts + setEvidenceList(evidences))
save("/users/kylehundman/desktop/output.json")
load("/users/kylehundman/desktop/output.json") #load back in saved node (after creation of full network)
evidences = getUserInput()  
doInference(cpts + setEvidenceList(evidences))
'''




