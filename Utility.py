'''
Computes the best possible score for the crowdsourced values
'''
def bestPossibleScore(crowdsourcedValues):
    total = 0
    for val in crowdsourcedValues.values():
        total += sum(sorted(val, reverse=True)[:3])
    return total

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
