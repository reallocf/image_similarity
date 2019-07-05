'''
Convert the imageMap with pixels (R, G, B) -> single value (R + G + B) / 3
'''
def grayOutImageMap(imageMap):
    grayImageMap = {}
    for imageId, pixelList in imageMap.items():
        grayImageMap[imageId] = [(r + g + b) / 3.0 for (r, g, b) in pixelList]
    return grayImageMap
