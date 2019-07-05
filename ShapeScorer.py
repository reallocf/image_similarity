import time

import Constants
import Utility

'''
Adjusts black/white cutoff from 0 to a configurable max to scan the
hyperparameter space to find the best number of black/white cutoff to select.

Used to find the (now set) bestShapeBorder value. Can be run again for
validation, but takes a long time (with a higher max bin count leading to a longer runtime).

Best score found: 3760 with shape border = 80
Time to process where max = 255 (entire probability space searched): ~4.5 minutes (264.949 seconds)

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
def hyperparameterTuneShapeDistances(imageMap, crowdsourcedValues):
    bestScore = 0
    bestParam = -1
    start = time.time()
    for shapeBorder in range(0, Constants.maxShapeBorder):
        print(f'Trying shape border: {shapeBorder}')
        currentScore = scoreShape(imageMap, crowdsourcedValues, shapeBorder)
        if currentScore > bestScore:
            bestScore = currentScore
            bestParam = shapeBorder
        print(f'Current score: {currentScore} ; Best score: {bestScore} ; Best score values: {bestParam}')
    end = time.time()
    print(f'The best histogram bin size is {bestParam}')
    print(f'Total time elapsed finding hyperparam: {end - start}')

'''
Score shape logic - can be run directly from main if known shape border
otherwise used in hyperparameter tuning
'''
def scoreShape(imageMap, crowdsourcedValues, shapeBorder):
    blackWhiteMap = transformIntoBlackWhiteMap(Utility.grayOutImageMap(imageMap), shapeBorder)
    shapeDistances = Utility.findDistances(blackWhiteMap, shapeDist, ())
    return Utility.findScoreFromCrowdsource(shapeDistances, crowdsourcedValues)

'''
Iterate over gray image map and transform values to 1 or 0 based on the passed
shape border
'''
def transformIntoBlackWhiteMap(grayImageMap, shapeBorder):
    blackWhiteMap = {}
    for imageId, grayPixels in grayImageMap.items():
        blackWhiteMap[imageId] = [0 if pix <= shapeBorder else 1 for pix in grayPixels]
    return blackWhiteMap

'''
Finds the texture distance between the two image histograms
'''
def shapeDist(imageBlackWhiteList, otherImageBlackWhiteList, hyperparams):
    totalDist = 0
    for i in range(len(imageBlackWhiteList)):
        totalDist += 1 if imageBlackWhiteList[i] != otherImageBlackWhiteList[i] else 0
    return totalDist * 2 # multiply by 2 because divided by 2 for l1norms in Utility.py
