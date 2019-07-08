magicHeader = b'P6\n#JDONtLJDO\n89 60\n255\n'
rows = 60
cols = 89
maxLaplaceVal = 2040.0 # 255 * 8
imagePath = "./images/i{0}.ppm"
crowdPath = "./Crowd.txt"
personalPath = "./cgs2161.txt"
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
minAVal = 0.5
maxAVal = 0.5
minBVal = 0.05
maxBVal = 0.05
minJointRedHistBins = 6
maxJointRedHistBins = 6
minJointGreenHistBins = 6
maxJointGreenHistBins = 6
minJointBlueHistBins = 10
maxJointBlueHistBins = 10
minJointTextureHistBins = 45
maxJointTextureHistBins = 45
minJointShapeBorder = 81
maxJointShapeBorder = 81
# Best values found for joint calculations
bestJointAVal = 0.5
bestJointBVal = 0.05
bestJointCVal = 0.45
bestJointRedBinCount = 6
bestJointGreenBinCount = 6
bestJointBlueBinCount = 10
bestJointTextureBinCount = 45
bestJointShapeBorder = 81
bestOverallParams = (bestJointAVal,
bestJointBVal,
bestJointCVal,
bestJointRedBinCount,
bestJointGreenBinCount,
bestJointBlueBinCount,
bestJointTextureBinCount,
bestJointShapeBorder)