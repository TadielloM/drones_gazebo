import os
import errno
import sys,getopt
import fileinput
import shutil
import re
import math

#CREATION OF THE DRONE MODELS
def main(argv):
    
    numCopies = 50
    CAalgorithm = 'ORCA'

    templateDir = './models/dronetemplate'
    copyDir = './models/'
    worldsDir = './worlds/'
    templateModelName = '{$modelName}'
    templatePose = '{$modelPose}'
    templateIP = '{$modelIP}'
    templateAlgorithm = '{$modelAlgorithm}'
    templateTest = '{$modelTest}'
    templateWorldModels = '{$models}'
    templateWorldName = '{$worldName}'
    modelName= 'drone'
    worldName= 'world'
    worldFileName= 'world_template.world'
    numTest =1
    radius = 5
    
    #Remove old files
    files = os.listdir(copyDir)
    for x in files:
        if (re.match("drone_.+",x)):
            shutil.rmtree(os.path.join(copyDir,x))
            print("Deleted "+x)

    files = os.listdir(worldsDir)
    for x in files:
        if (re.match("drones_.+.world",x)):
            os.remove(os.path.join(worldsDir,x))
            print("Deleted "+x)

    confFileName= 'model.config'
    sdfFileName = 'model.sdf'

    confFile = open(os.path.join(templateDir,confFileName),'r')
    sdfFile = open(os.path.join(templateDir,sdfFileName),'r')
    alpha= 0
    #Create new drones
    for i in range(1,numCopies+1):
        for t in [1,2,3]:
            newModelName = modelName+"_"+str(i)+"_"+str(t)
            newDir = os.path.join(copyDir,newModelName)
            os.makedirs(newDir)

            newConfFile = open(os.path.join(newDir,confFileName),'w')
            for line in confFile:
                newConfFile.write(line.replace(templateModelName,newModelName))
            newConfFile.close()
            confFile.seek(0,0)

            #modify the template file with the correct names
            newSdfFile = open(os.path.join(newDir,sdfFileName),'w')
            for line in sdfFile:
                if templatePose in line:
                    if(numTest == 1):
                        num = (numCopies-i)*2
                        newSdfFile.write(line.replace(templatePose, (str(num) +' 0 20')))
                    elif numTest == 2:
                        alpha = (((360/(numCopies-1))*(i-1))* math.pi/180)+math.pi
                        newSdfFile.write(line.replace(templatePose, (str(radius*math.cos(alpha)) +' '+str(radius*math.sin(alpha))+' 10')))
                    elif numTest == 2:
                        alpha = (((360/(numCopies-1))*(i-1))* math.pi/180)+math.pi
                        newSdfFile.write(line.replace(templatePose, (str(radius*math.cos(alpha)) +' '+str(radius*math.sin(alpha))+' 10')))
                elif templateIP in line:
                    newSdfFile.write(line.replace(templateIP, '127.0.0.'+str(i)))
                elif templateAlgorithm in line:
                    newSdfFile.write(line.replace(templateAlgorithm, CAalgorithm ))
                elif templateTest in line:
                    newSdfFile.write(line.replace(templateTest, str(numTest) ))
                else:
                    newSdfFile.write(line.replace(templateModelName,newModelName))
            newSdfFile.close()
            sdfFile.seek(0,0)

    confFile.close()
    sdfFile.close()

    #CREATION OF THE WORLD FILE
    tests=[5,10,15,20,30,40,50]
    for n in tests:
        for t in [1,2,3]:
            worldFile = open(os.path.join(worldsDir,worldFileName),'r')
            newWorldName = "drones_"+str(n)+"_"+str(t)+".world"
            newWorldFile = open(os.path.join(worldsDir,newWorldName),'w')
            models=""
            for i in range(1,n+1):
                if numTest==1 :
                    models+="\r\t\t<include>\n\t\t\t<name>drone_"+str(i)+"_"+str(t)+"</name>\n\t\t\t<uri>model://drone_"+str(i)+"_"+str(t)+"</uri>\n\t\t\t<pose>"+str((i-1)*2)+" 0 10 0 0 0</pose>\n\t\t</include>\n"
                else:
                    alpha = i*((2*math.pi)/(n))            
                    models+="\r\t\t<include>\n\t\t\t<name>drone_"+str(i)+"_"+str(t)+"</name>\n\t\t\t<uri>model://drone_"+str(i)+"_"+str(t)+"</uri>\n\t\t\t<pose>"+str(radius*math.cos(alpha))+" "+str(radius*math.sin(alpha))+" 10 0 0 0</pose>\n\t\t</include>\n"
                
            
            for line in worldFile:
                if templateWorldModels in line:
                    newWorldFile.write(line.replace(templateWorldModels,models))
                elif templateWorldName in line:
                    newWorldFile.write(line.replace(templateWorldName, worldName+'_'+str(n)))
                else:
                    newWorldFile.write(line)
            newWorldFile.close()
            worldFile.seek(0,0)

if __name__ == "__main__":
    main(sys.argv[1:])
