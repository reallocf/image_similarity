magicHeader = b'P6\n#JDONtLJDO\n89 60\n255\n'
rows = 60
cols = 89
maxLaplaceVal = 2040.0 # 255 * 8
imagePath = "./images/i{0}.ppm"
crowdPath = "./Crowd.txt"
# Max values for individual calculations
maxColorHistBins = 14
maxTextureHistBins = 100
maxShapeBorder = 255
# Best values found for individual calculations
bestRedBinCount = 13
bestGreenBinCount = 7
bestBlueBinCount = 1
bestTextureBinCount = 45
bestShapeBorder = 80
# Max and min values for joint calculations
minJointColorHistBins = 8
maxJointColorHistBins = 8
minJointTextureHistBins = 45
maxJointTextureHistBins = 45
minJointShapeBorder = 80
maxJointShapeBorder = 80
# Best values found for joint calculations
bestJointAVal = 0.5
bestJointBVal = 0.05
bestJointCVal = 0.45
bestJointRedBinCount = 8
bestJointGreenBinCount = 8
bestJointBlueBinCount = 8
bestJointTextureBinCount = 45
bestJointShapeBorder = 80
bestOverallParams = (bestJointAVal,
bestJointBVal,
bestJointCVal,
bestJointRedBinCount,
bestJointGreenBinCount,
bestJointBlueBinCount,
bestJointTextureBinCount,
bestJointShapeBorder)