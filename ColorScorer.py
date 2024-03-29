import time

import Constants
import Utility

'''
Adjusts the bin count from 0 to a configurable max to scan the bin
hyperparameter space to find the best number of histogram bins to select.

Used to find the (now set) bestRedBinCount, bestGreenBinCount, and
bestBlueBinCount values. Can be run again for validation, but takes a long time
(with a higher max bin count leading to a longer runtime).

Best score found: 3534 with red = 13, green = 7, blue = 1
Time to process where max = 14: ~15 minutes (867.856 seconds)

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
def hyperparameterTuneColorDistances(imageMap, crowdsourcedValues, personalValues):
    bestScore = 0
    bestParams = (-1, -1, -1)
    start = time.time()
    for redBinCount in range(1, Constants.maxColorHistBins + 1):
        for greenBinCount in range(1, Constants.maxColorHistBins + 1):
            for blueBinCount in range(1, Constants.maxColorHistBins + 1):
                print(f'Trying red: {redBinCount} ; green: {greenBinCount} ; blue: {blueBinCount}')
                currentScore = scoreColor(imageMap, crowdsourcedValues, personalValues, redBinCount, greenBinCount, blueBinCount)
                if currentScore > bestScore:
                    bestScore = currentScore
                    bestParams = (redBinCount, greenBinCount, blueBinCount)
                print(f'Current score: {currentScore} ; Best score: {bestScore} ; Best score values: {bestParams}')
    end = time.time()
    print(f'The best histogram bin sizes are {bestParams}')
    print(f'Total time elapsed finding hyperparams: {end - start}')

'''
Score color logic - can be run directly from main if known bin counts
otherwise used in hyperparameter tuning
'''
def scoreColor(imageMap, crowdsourcedValues, personalValues, redHistBins, greenHistBins, blueHistBins):
    imageHistMap = transformIntoColorHistograms(imageMap, redHistBins, greenHistBins, blueHistBins)
    colorDistances = Utility.findDistances(imageHistMap, colorDist, (redHistBins, greenHistBins, blueHistBins))
    Utility.reportHappinessScore(colorDistances, personalValues)
    return Utility.findScoreFromCrowdsource(colorDistances, crowdsourcedValues)

'''
Encodes the image map into a RGB histogram with the given bin counts
Input:
- imageMap: a map of image ids to encoded images (list of sequential RGB bytes)
- redHistBins: the number of red histogram bins
- greenHistBins: the number of green histogram bins
- blueHistBins: the number of blue histogram bins
Output:
a map of image ids to histogram-encoded images
'''
def transformIntoColorHistograms(imageMap, redHistBins, greenHistBins, blueHistBins):
    imageHistMap = {}
    for imageId, imagePixels in imageMap.items():
        imageHistList = [[[0 for x in range(blueHistBins)] for x in range(greenHistBins)] for x in range(redHistBins)]
        for pixel in imagePixels:
            imageHistList[pixel[0] % redHistBins][pixel[1] % greenHistBins][pixel[2] % blueHistBins] += 1
        imageHistMap[imageId] = imageHistList
    return imageHistMap

'''
Finds the color distance between two image histograms
'''
def colorDist(imageHist, otherImageHist, hyperparams):
    totalDist = 0
    redHistBins, greenHistBins, blueHistBins = hyperparams
    for r in range(redHistBins):
        for g in range(greenHistBins):
            for b in range(blueHistBins):
                totalDist += abs(imageHist[r][g][b] - otherImageHist[r][g][b])
    return totalDist
