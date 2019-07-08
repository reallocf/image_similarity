import time

import ColorScorer
import Constants
import ShapeScorer
import TextureScorer
import Utility

'''
Adjusts all the hyperparameters. The big kahuna.

Used to find the (now set) bestJoint... values. Can be run again for validation, but takes a long time
(with larger max/min ranges leading to longer runtimes).

Best score found: 5683 with a = 5, b = 0.05, c = 0.45
Time to process: ~9 minutes (523.722 seconds)

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
def hyperparameterTuneOverallDistances(imageMap, crowdsourcedValues, personalValues):
    bestScore = 0
    bestParams = (-1, -1, -1, -1, -1, -1, -1, -1)
    start = time.time()
    aVal = Constants.minAVal
    bVal = Constants.minBVal
    while aVal <= Constants.maxAVal:
        while bVal <= Constants.maxBVal:
            cVal = 1.0 - aVal - bVal
            if cVal < 0:
                bVal += 0.05
                continue
            for redBinCount in range(Constants.minJointRedHistBins, Constants.maxJointRedHistBins + 1):
                for greenBinCount in range(Constants.minJointGreenHistBins, Constants.maxJointGreenHistBins + 1):
                    for blueBinCount in range(Constants.minJointBlueHistBins, Constants.maxJointBlueHistBins + 1):
                        for textureBinCount in range(Constants.minJointTextureHistBins, Constants.maxJointTextureHistBins + 1):
                            for shapeBorder in range(Constants.minJointShapeBorder, Constants.maxJointShapeBorder + 1):
                                print(f'A: {aVal} ; B: {bVal} ; C: {cVal} ; R: {redBinCount} ; G: {greenBinCount} ; B: {blueBinCount} ; T {textureBinCount} ; S {shapeBorder}')
                                params = (aVal, bVal, cVal, redBinCount, greenBinCount, blueBinCount, textureBinCount, shapeBorder)
                                currentScore = scoreOverall(imageMap, crowdsourcedValues, personalValues, params)
                                if currentScore > bestScore:
                                    bestScore = currentScore
                                    bestParams = params
                                print(f'Current score: {currentScore} ; Best score: {bestScore} ; Best score values: {bestParams}')
            bVal += 0.05
        bVal = Constants.minBVal
        aVal += 0.05
    end = time.time()
    print(f'The best histogram bin sizes are {bestParams}')
    print(f'Total time elapsed finding hyperparams: {end - start}')

'''
Score shape logic - can be run directly from main if known shape border
otherwise used in hyperparameter tuning
'''
def scoreOverall(imageMap, crowdsourcedValues, personalValues, hyperparams):
    overallMap = transformOverallMap(imageMap, hyperparams)
    overallDistances = Utility.findDistances(overallMap, overallDist, hyperparams)
    Utility.reportHappinessScore(overallDistances, personalValues)
    return Utility.findScoreFromCrowdsource(overallDistances, crowdsourcedValues)

'''
Iterate over gray image map and transform values to 1 or 0 based on the passed
shape border
'''
def transformOverallMap(imageMap, hyperparams):
    overallMap = {}
    _, _, _, redBinCount, greenBinCount, blueBinCount, textureBinCount, shapeBorder = hyperparams
    colorHistMap = ColorScorer.transformIntoColorHistograms(imageMap, redBinCount, greenBinCount, blueBinCount)
    textureHistMap = TextureScorer.transformIntoLaplaceHistograms(imageMap, textureBinCount)
    shapeBlackAndWhiteMap = ShapeScorer.transformIntoBlackWhiteMap(imageMap, shapeBorder)
    for imageId, colorHist in colorHistMap.items():
        overallMap[imageId] = (colorHist, textureHistMap[imageId], shapeBlackAndWhiteMap[imageId])
    return overallMap

'''
Finds the overall distance between the two images
'''
def overallDist(imageEncodings, otherImageEncodings, hyperparams):
    colorEncoding, textureEncoding, shapeEncoding = imageEncodings
    otherColorEncoding, otherTextureEncoding, otherShapeEncoding = otherImageEncodings
    aVal, bVal, cVal, redBinCount, greenBinCount, blueBinCount, textureBinCount, shapeBorder = hyperparams
    overallDist = aVal * ColorScorer.colorDist(colorEncoding, otherColorEncoding, (redBinCount, greenBinCount, blueBinCount))
    overallDist += bVal * TextureScorer.textureDist(textureEncoding, otherTextureEncoding, (textureBinCount))
    overallDist += cVal * ShapeScorer.shapeDist(shapeEncoding, otherShapeEncoding, (shapeBorder))
    return overallDist
