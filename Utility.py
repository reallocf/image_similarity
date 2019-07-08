import sys

import Constants

'''
Computes the best possible score for the crowdsourced values
'''
def bestPossibleScore(crowdsourcedValues):
    total = 0
    for val in crowdsourcedValues.values():
        total += sum(sorted(val, reverse=True)[:3])
    return total

'''
Finds the 3 "closest" images for each image (calculated via L1 norm)
Input:
- imageValueMap: a map of image ids to images encoded as some value (histogram, pixels, etc.)
- distCalculator: function that sums the values between the two histograms
- hyperparams: hyperparameters to feed into distCalculator
Output:
a map of color distances of this format:
{
    01 : [selection1, selection2, selection3],
    02 : [selection1, selection2, selection3],
    ...
    40 : [selection1, selection2, selection3]
}
where each selection is the closest calculated color (smallest L1 dist)
'''
def findDistances(imageValueMap, distCalculator, hyperparams):
    colorDistMap = {}
    for imageId, imageVal in imageValueMap.items():
        closestThree = [-1, -1, -1]
        closestThreeDists = [sys.maxsize, sys.maxsize, sys.maxsize]
        for otherImageId, otherImageVal in imageValueMap.items():
            if imageId == otherImageId:
                continue # image shouldn't be compared to itself
            l1Dist = distCalculator(imageVal, otherImageVal, hyperparams) / (2.0 * Constants.rows * Constants.cols)
            potentiallySwapInNewDist(closestThree, closestThreeDists, otherImageId, l1Dist)
        colorDistMap[imageId] = closestThree
    return colorDistMap


'''
Given the new image added, swap it into the correct position in closestThree
and closestThreeDists such that both are in decreasing order of dist
'''
def potentiallySwapInNewDist(closestThree, closestThreeDists, otherImageId, otherImageDist):
    if otherImageDist < closestThreeDists[0]:
        closestThree[2] = closestThree[1]
        closestThreeDists[2] = closestThreeDists[1]
        closestThree[1] = closestThree[0]
        closestThreeDists[1] = closestThreeDists[0]
        closestThree[0] = otherImageId
        closestThreeDists[0] = otherImageDist
    elif otherImageDist < closestThreeDists[1]:
        closestThree[2] = closestThree[1]
        closestThreeDists[2] = closestThreeDists[1]
        closestThree[1] = otherImageId
        closestThreeDists[1] = otherImageDist
    elif otherImageDist < closestThreeDists[2]:
        closestThree[2] = otherImageId
        closestThreeDists[2] = otherImageDist

'''
Given the distances and the crowdsourced values, come up with a numeric
score for how well this particular distance matches the "ground truth"
crowdsourced values
Input:
- distances: a map of distances of this format:
{
    01 : [selection1, selection2, selection3],
    02 : [selection1, selection2, selection3],
    ...
    40 : [selection1, selection2, selection3]
}
where each selection is the closest calculated color (smallest L1 dist)
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
def findScoreFromCrowdsource(distances, crowdsourcedValues):
    totalScore = 0
    for image, selectionList in distances.items():
        crowdsourcedValuesList = crowdsourcedValues.get(image)
        sel1Dist = crowdsourcedValuesList[selectionList[0] - 1]
        sel2Dist = crowdsourcedValuesList[selectionList[1] - 1]
        sel3Dist = crowdsourcedValuesList[selectionList[2] - 1]
        totalScore += sel1Dist + sel2Dist + sel3Dist
    return totalScore

'''
Convert the imageMap with pixels (R, G, B) -> single value (R + G + B) / 3
'''
def grayOutImageMap(imageMap):
    grayImageMap = {}
    for imageId, pixelList in imageMap.items():
        grayImageMap[imageId] = [(r + g + b) / 3.0 for (r, g, b) in pixelList]
    return grayImageMap

'''
Given an X and Y, find the corresponding value in the linearized image
'''
def getXYVal(image, x, y):
    if x < 0 or y < 0 or x == Constants.rows or y == Constants.cols:
        return 0
    else:
        return image[(x * Constants.rows) + y]

'''
Report a happiness score 0-120 with an additional 1 being for every found image
that I selected in cgs2161.txt
'''
def reportHappinessScore(distances, personalValues):
    happinessScore = 0
    for image, selectionList in distances.items():
        personalValuesSet = set(personalValues.get(image))
        for selection in selectionList:
            if selection in personalValuesSet:
                happinessScore += 1
    print(f'Happiness score is {happinessScore}')
