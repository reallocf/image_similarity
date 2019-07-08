import Constants

'''
Given the path to the image files, read them in to output a map like:
{
    01: [(pix1RedVal, pix1GreenVal, pix1BlueVal), ...]
    02: [(pix1RedVal, pix1GreenVal, pix1BlueVal), ...]
    ...
    40: [(pix1RedVal, pix1GreenVal, pix1BlueVal), ...]
}
where each list has cols * rows number of length 3 tuples representing pixels
'''
def encodeImagesAsPixelListMap(imagePath):
    imageMap = {}
    for i in range(1, 41):
        thisImagePath = imagePath.format(i if i >= 10 else f'0{i}')
        pixelList = []
        with open(thisImagePath, "rb") as f:
            test = f.read(24)
            assert test == Constants.magicHeader
            r = f.read(1)
            while r != b"":
                g = f.read(1)
                b = f.read(1)
                pixelList.append((int.from_bytes(r, byteorder='big'), int.from_bytes(g, byteorder='big'), int.from_bytes(b, byteorder='big')))
                r = f.read(1)
        assert len(pixelList) == Constants.cols * Constants.rows
        imageMap[i] = pixelList
    return imageMap

'''
Generate a map of crowdsourced values from Crowd.txt of this format:
{
    01 : [bordaCountIm01, bordaCountIm02, ..., bordaCountIm40],
    02 : [bordaCountIm01, bordaCountIm02, ..., bordaCountIm40],
    ...
    40 : [bordaCountIm01, bordaCountIm02, ..., bordaCountIm40]
}
where bordaCountIm01 is the borda count as calculated in the spec
'''
def readInCrowdsourcedValues(crowdPath):
    crowdsourcedValues = {}
    with open(crowdPath) as f:
        content = f.readlines()
        for i in range(1, len(content) + 1):
            vals = [int(x) for x in content[i - 1].split()]
            assert len(vals) == 40
            crowdsourcedValues[i] = vals
    assert len(crowdsourcedValues) == 40
    return crowdsourcedValues

'''
Generate a map of personal values from cgs2161.txt of this format:
{
    01 : [mySelection1, mySelection2, mySelection3]
    02 : [mySelection1, mySelection2, mySelection3]
    ...
    40 : [mySelection1, mySelection2, mySelection3]
}
'''
def readInPersonalValues(personalPath):
    personalValues = {}
    with open(personalPath) as f:
        content = f.readlines()
        for i in range(1, len(content) + 1):
            vals = [int(x) for x in content[i - 1].split()]
            assert(i == vals[0])
            personalValues[i] = vals[1:]
    assert len(personalValues) == 40
    return personalValues
