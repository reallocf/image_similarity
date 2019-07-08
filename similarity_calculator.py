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
    personalValues = FileHandler.readInPersonalValues(Constants.personalPath)

    # Calculate and print best possible score
    print(Utility.bestPossibleScore(crowdsourcedValues))

    # Calculate and print my personal score
    print(Utility.findScoreFromCrowdsource(personalValues, crowdsourcedValues))

    # Tune color hyperparameters - TAKES A LONG TIME
    #ColorScorer.hyperparameterTuneColorDistances(imageMap, crowdsourcedValues, personalValues)

    # Prints out the total color score with the configured histogram bin counts
    print(ColorScorer.scoreColor(imageMap, crowdsourcedValues, personalValues, Constants.bestRedBinCount, Constants.bestGreenBinCount, Constants.bestBlueBinCount))

    # Tune texture hyperparameters
    #TextureScorer.hyperparameterTuneTextureDistances(imageMap, crowdsourcedValues, personalValues)

    # Prints out the total texture score with the configured histogram count
    print(TextureScorer.scoreTexture(imageMap, crowdsourcedValues, personalValues, Constants.bestTextureBinCount))

    # Tune shape hyperparameters
    #ShapeScorer.hyperparameterTuneShapeDistances(imageMap, crowdsourcedValues, personalValues)

    # Prints out the total shape score with the configured shape border
    print(ShapeScorer.scoreShape(imageMap, crowdsourcedValues, Constants.bestShapeBorder, personalValues))

    # Tune all hyperparameters - TAKES A LOONG LONG LOOOONG TIME depending on set params
    #OverallScorer.hyperparameterTuneOverallDistances(imageMap, crowdsourcedValues, personalValues)

    # Prints out the total overall score with the params configured in Constants
    print(OverallScorer.scoreOverall(imageMap, crowdsourcedValues, personalValues, Constants.bestOverallParams))
