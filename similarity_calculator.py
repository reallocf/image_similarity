import ColorScorer
import Constants
import FileHandler
import OverallScorer
import ShapeScorer
import TextureScorer
import Utility

if __name__ == "__main__":
    # Prepare image map and crowdsourced values
    imageMap = FileHandler.encodeImagesAsPixelListMap(Constants.imagePath)
    crowdsourcedValues = FileHandler.readInCrowdsourcedValues(Constants.crowdPath)

    # Calculate and print best possible score
    #print(Utility.bestPossibleScore(crowdsourcedValues))

    # Tune color hyperparameters - TAKES A LONG TIME
    #ColorScorer.hyperparameterTuneColorDistances(imageMap, crowdsourcedValues)

    # Prints out the total color score with the configured histogram bin counts
    #print(ColorScorer.scoreColor(imageMap, crowdsourcedValues, Constants.bestRedBinCount, Constants.bestGreenBinCount, Constants.bestBlueBinCount))

    # Tune texture hyperparameter
    #TextureScorer.hyperparameterTuneTextureDistances(imageMap, crowdsourcedValues)

    # Prints out the total texture score with the configured histogram count
    #print(TextureScorer.scoreTexture(imageMap, crowdsourcedValues, Constants.bestTextureBinCount))

    # Tune shape hyperparameter
    #ShapeScorer.hyperparameterTuneShapeDistances(imageMap, crowdsourcedValues)

    # Prints out the total shape score with the configured shape border
    #print(ShapeScorer.scoreShape(imageMap, crowdsourcedValues, Constants.bestShapeBorder))

    # Tune all hyperparameters
    #OverallScorer.hyperparameterTuneOverallDistances(imageMap, crowdsourcedValues)

    # Prints out the total overall score with the params configured in Constants
    print(OverallScorer.scoreOverall(imageMap, crowdsourcedValues, Constants.bestOverallParams))
