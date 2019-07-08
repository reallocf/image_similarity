import math
import time

import Constants
import Utility

'''
Adjusts the bin count from 0 to a configurable max to scan the bin
hyperparameter space to find the best number of histogram bin count to select.

Used to find the (now set) bestTextureBinCount value. Can be run again for
validation, but takes a long time (with a higher max bin count leading to a longer runtime).

Best score found: 2397 with texture hist bins = 45
Time to process where max = 100: ~2 minutes (121.787 seconds)

Input:
- imageMap: a map of image ids to encoded images (list of sequential RGB bytes)
- crowdsourcedValues: a map of crowdsourced values of this format:
{
    01 : [bordaCountIm01, bordaCountIm02, ..., bordaCountIm40],
    02 : [bordaCountIm01, bordaCountIm02, ..., bordaCountIm40],
    ...
    40 : [bordaCountIm01, bordaCountIm02, ..., bordaCountIm40]
}
where bordaCountIm01 is the borda count as calculated in the spec (retrieved
directly from Crowd.txt)
'''
def hyperparameterTuneTextureDistances(imageMap, crowdsourcedValues, personalValues):
    bestScore = 0
    bestParam = -1
    start = time.time()
    for textureBinCount in range(1, Constants.maxTextureHistBins + 1):
        print(f'Trying texture: {textureBinCount}')
        currentScore = scoreTexture(imageMap, crowdsourcedValues, personalValues, textureBinCount)
        if currentScore > bestScore:
            bestScore = currentScore
            bestParam = textureBinCount
        print(f'Current score: {currentScore} ; Best score: {bestScore} ; Best score values: {bestParam}')
    end = time.time()
    print(f'The best histogram bin size is {bestParam}')
    print(f'Total time elapsed finding hyperparam: {end - start}')

'''
Score texture logic - can be run directly from main if known bin count
otherwise used in hyperparameter tuning
'''
def scoreTexture(imageMap, crowdsourcedValues, personalValues, textureHistBins):
    laplaceHistMap = transformIntoLaplaceHistograms(imageMap, textureHistBins)
    textureDistances = Utility.findDistances(laplaceHistMap, textureDist, (textureHistBins))
    Utility.reportHappinessScore(textureDistances, personalValues)
    return Utility.findScoreFromCrowdsource(textureDistances, crowdsourcedValues)

'''
Run a laplace transformation over each image then add them into different
histogram buckets
'''
def transformIntoLaplaceHistograms(imageMap, textureHistBins):
    laplaceHistMap = {}
    for imageId, grayPixels in Utility.grayOutImageMap(imageMap).items():
        laplaceList = [0 for x in range(textureHistBins)]
        for x in range(Constants.rows):
            for y in range(Constants.cols):
                laplaceVal = abs(
                    Utility.getXYVal(grayPixels, x, y) * -8
                    + Utility.getXYVal(grayPixels, x - 1, y - 1)
                    + Utility.getXYVal(grayPixels, x - 1, y)
                    + Utility.getXYVal(grayPixels, x - 1, y + 1)
                    + Utility.getXYVal(grayPixels, x, y - 1)
                    + Utility.getXYVal(grayPixels, x, y + 1)
                    + Utility.getXYVal(grayPixels, x + 1, y - 1)
                    + Utility.getXYVal(grayPixels, x + 1, y)
                    + Utility.getXYVal(grayPixels, x + 1, y + 1)
                    )
                laplaceList[math.floor((laplaceVal / Constants.maxLaplaceVal) * textureHistBins)] += 1
        laplaceHistMap[imageId] = laplaceList
    return laplaceHistMap

'''
Finds the texture distance between the two image histograms
'''
def textureDist(imageHist, otherImageHist, hyperparams):
    totalDist = 0
    textureHistBins = hyperparams
    for t in range(textureHistBins):
        totalDist += abs(imageHist[t] - otherImageHist[t])
    return totalDist
