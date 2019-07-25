import csv
import math
import random


def loadCSV():
    lines = csv.reader(open(r'C:\Users\drilo\PycharmProjects\DataMining\CancerDB.csv'))
    dataset = list(lines)
    for i in range(len(dataset)):
        dataset[i] = [float(x) for x in dataset[i]]
    return dataset


def splitDataset(dataset, splitRadio):
    trainSize = int(len(dataset) * splitRadio)
    trainSet = []
    copy = list(dataset)
    while len(trainSet) < trainSize:
        index = random.randrange(len(copy))
        trainSet.append(copy.pop(index))
    return [trainSet, copy]


def seperateByClass(dataset):
    seperate = {}
    for i in range(len(dataset)):
        vector = dataset[i]
        if vector[-1] not in seperate:
            seperate[vector[-1]] = []
        seperate[vector[-1]].append(vector)
    return seperate


def mean(numbers):
    return sum(numbers) / float(len(numbers))


def stdev(numbers):
    avg = mean(numbers)
    variance = sum([pow(x - avg, 2) for x in numbers]) / float(len(numbers) - 1)
    return math.sqrt(variance)


def summarize(dataset):
    summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataset)]
    del summaries[-1]
    return summaries


def summarizeByClass(dataset):
    seperated = seperateByClass(dataset)
    summariez = {}
    for classValue, instances in seperated.items():
        summariez[classValue] = summarize(instances)
    return summariez


def calculateProbability(x, mean, stdev):
    exponent = math.exp(-(math.pow(x - mean, 2)) / (2 * math.pow(stdev, 2)))
    return (1 / (math.sqrt(2 * math.pi) * stdev)) * exponent


def calculateClassProbability(summaries, inputVector):
    probabilities = {}
    for classValue, classSummaries in summaries.items():
        probabilities[classValue] = 1
        for i in range(len(classSummaries)):
            mean, stdev = classSummaries[i]
            x = inputVector[i]
            probabilities[classValue] *= calculateProbability(x, mean, stdev)
        return probabilities


def predict(summaries, inputVector):
    probabilities = calculateClassProbability(summaries, inputVector)
    bestLabel, bestProb = None, -1
    for classValue, probability in probabilities.items():
        if (bestLabel is None or probability > bestProb):
            bestProb = probability
            bestLabel = classValue
    return bestLabel


def getPredictions(summaries, testSet):
    predictions = []
    for i in range(len(testSet)):
        result = predict(summaries, testSet[i])
        predictions.append(result)
    return predictions


def getAccuracy(testSet, predictions):
    correct = 0
    list2 = []
    for x in range(len(testSet)):
        list2.append('{} -> {} (expected {}) , {}'.format(remove0(removalLastIndex(testSet[x])), benorMen(testSet[x][-1]),
                                                   benorMen(predictions[x]), correctIncorrect(benorMen(testSet[x][-1]),
                                                                                              benorMen(predictions[x]))))
        if testSet[x][-1] == predictions[x]:
            correct += 1
    return ((correct / float(len(testSet))) * 100.0 ) , list2


def remove0(list):
    list2 = []
    for i in list:
        list2.append(int(i))
    return list2


def correctIncorrect(str1, str2):
    if str1 == str2:
        return 'CORRECT'
    return 'INCORRECT'


def benorMen(number):
    if number == 2 or number == 2.0:
        return 'benign'
    return 'malignant'


def removalLastIndex(list):
    list2 = []
    i = 0
    for x in list:
        if i < (len(list) - 1):
            list2.append(x)
            i += 1
    return list2


def main():
    accur = 0
    list = []
    d = 1000
    for i in range(d):
        dataset = loadCSV()
        trainingSet, testSet = splitDataset(dataset, splitRadio=0.72)
        summaries = summarizeByClass(trainingSet)
        predictions = getPredictions(summaries, testSet)
        accuracy = getAccuracy(testSet, predictions)

        if accur == 0 or accur < accuracy[0]:
            accur = accuracy[0]
            list = accuracy[1]
    print('Rasti me i mire nga ' , d , ' raste :')
    for i in list:
        print(i)
    print('Accucracy : {}%'.format(accur))


if __name__ == '__main__':
    main()
