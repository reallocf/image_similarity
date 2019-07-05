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
bestRedBinCount = 8
bestGreenBinCount = 7
bestBlueBinCount = 7
bestTextureBinCount = 45
bestShapeBorder = 80
# Max and min values for joint calculations
# Best values found for joint calculations