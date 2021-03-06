import types, os
import time
import math,struct
import statc
import string
import orngStat
import copy
import orngTest
import orange
import numpy
import commands
from statlib import stats
from AZutilities import miscUtilities
from AZutilities import dataUtilities
from rdkit import Chem
from rdkit.Chem import Draw
version = 2
verbose = 0

CLASSIFICATION = 1  # 0b00000001
REGRESSION = 2      # 0b00000010

def tanimotoSimilarity(A, B):
    """Calculates the tanimnoto similarity defined by:
             ts = c/(a+b-c)
        where a is the number of bits in A
              b is the number of bits in B
              c is the number of bits in common
             
        A and B are the strings containing the bits
        This returns a value between 0 and 1:
                0 - Nothing in common
                1 - Identical
        len(A) and len(A) and len(B) are expected to be the same
    """
    #Not validating input since this function has to called very often.
    nAB = 0.0 + miscUtilities.countOnBits(int(A,2) & int(B,2))
    nAnB = A.count("1") + B.count("1")
    if not nAnB: return 0.0
    else: return  nAB / (nAnB - nAB)

def fastTanimotoSimilarity(A,nA,B):
    """Same as tanimotoSimilarity but expecting in A and B a long integer representing the binary fingetprint
       and nA the number of ONbits in A"""
    #Not validating input since this function has to called very often.
    AandB = A & B
    nAB = miscUtilities.countOnBits(AandB)      # Number of match ON Bits
    nAnB = 0.0 + nA + miscUtilities.countOnBits(B)            # nA+nB
    if not nAnB: return 0.0
    else: return  nAB / (nAnB - nAB)



def getNearestNeighbors(query, n, NNDataPath, FPPath = None, resPath = None, idx = 0):
    """ get the n nearest neighbors
        query: bin string with query fingerprint
        returns an ordered list with the n top neighbors (each one in a dict):
            [ {
                "id"          : ID, 
                "expVal"      : ExpValues, 
                "similarity"  : TanimotoSimilarity, 
                "smi"         : smiles, 
                "imgPath"     : imgPath,
                "MeanInhib"   : Mean Inhib. },  ... ]        

        It will saves the images in resPath:
             NN_1.png    #1 neighbor
             NN_2.png    #2 neighbor
             ...
             NN_n.png    #n neighbor
    """
    if not query or not n or not  NNDataPath or not  FPPath:
        return []
    #if resPath and not os.path.isdir(resPath):
    #    os.makedirs(resPath)

    # get the correct header
    file = open(NNDataPath,"r")
    header = file.readline().strip().split('\t')
    file.close()

    if "Molecule SMILES" not in header or "Compound Name" not in header:
        print "NN dataset ",NNDataPath, " have not the correct header. It must contain 'Molecule SMILES' and 'Compound Name' attributes."
        return [] 
    # Index will have to be sum 1 because the TS will be prepended
    idxID = header.index("Compound Name") + 1
    idxExpVal = len(header) 
    idxSMILES = header.index("Molecule SMILES") + 1
    idxSimilarity = 0


    Nbits = 2048
    cmdStr = 'echo "' + query + '" | fpin ' + FPPath + " "  +NNDataPath + ' 0.0 '+str(n)
    status,output = commands.getstatusoutput(cmdStr)
    if status:
        print status
        print output
        raise Exception(str(output))
    #             TS              SMILES                    AZID         DATE       expRes
    # output = "0.7117   CCCC(C)C1(C(=O)NC(=O)NC1=O)CC   AZ10046012   2009-12-02   3.480007"
    TS=[]
    for ts in output.split("\n"):
        TS.append(ts.strip().split('\t'))
    # in TS:
    #    TS[n][0] - tanimoto similarity
    #    TS[n][1] - SMILES
    #    TS[n][2] - AZID
    #    TS[n][-1]- expRes
    res = []
    timeStamp=str(time.time()).replace(".",'')
    for fidx,nn in enumerate(TS):
        ID= nn[idxID]
        if miscUtilities.isNumber(nn[idxExpVal]):
            expVal = str(round(float(nn[idxExpVal]),2))
        else:
            expVal = nn[idxExpVal]
        SMILES = nn[idxSMILES]
        if resPath and os.path.isdir(resPath):
            imgPath = os.path.join(resPath,"NN"+str(idx)+"_"+str(fidx+1)+"_"+timeStamp+".png")
            mol = Chem.MolFromSmiles(SMILES)
            # save the respective imgPath...  
            Draw.MolToImageFile(mol,imgPath,size=(300, 300), kekulize=True, wedgeBonds=True)
        else:
            imgPath = ""
        res.append( {
                "id": ID, 
                "expVal": expVal, 
                "similarity": nn[idxSimilarity], 
                "smi": SMILES, 
                "imgPath": imgPath,
                "MeanInhib": ''} )
    return res
    

def calcConfMat(exp_pred_Val, labels):
    #exp_pred_Val is a list of lists of strings:
    #    [[exp_Val, pred_val],
    #     [exp_Val, pred_val],
    #    ...
    #    ]
    #labels is a list of strings which are the possible class lables ordered as in the original data.domain.classvar.values
    # The order of the matrix will be acconding to the order of the labels
    # the output will follow what defined in confMat method.
    CM = [[0]*len(labels) for x in range(len(labels))]
    for val in exp_pred_Val:
        row = labels.index(val[0])  # experimental
        col = labels.index(val[1])  # Predicted
        CM[row][col] += 1
    return [CM]
        


def ConfMat(res = None):
        """ Returns a confusion matrix in the form of a vector:
                For Binary classifiers:  
                        [[TP, FN],
                         [FP, TN]]
                For classifiers with class having N values:
                                             Predicted class
                                        |   A       B       C
                                     ---------------------------
                       experimental  A  |  tpA     eAB     eAC     eAB is read as: Error, should be A instead of B
                          class      B  |  eBA     tpB     eBC                
                                     C  |  eCA     eCB     tpC

                    [[tpA, eAB, ..., eAN],
                     [eBA, tpB, ..., eBN],
                      ...,
                     [eNA, eNB, ..., tpN ]]

                 where A, B, C are the class values in the same order as testData.domain.classVar.values
        """
        if res == None:
            return {"type":CLASSIFICATION}

        confMat_s = orngStat.confusionMatrices(res)
        retCM = []
        for confMat in confMat_s:
            if len(res.classValues) == 2:
                # NOTE: orngStat returns TN, TP, FN, FP with inverted labels, so we have to set properly:
                cm = [[confMat.TN, confMat.FP],[confMat.FN, confMat.TP]]
            else:
                cm = confMat
            retCM.append(cm)
        return retCM

def getConfMat(testData, model):
        return ConfMat(testOnData([model], testData))[0]

def calcKappa(_CM):
    """Returns the Kappa statistical coefficient for the agreement between measured and predicted classes"""
    def calcClassAccuracy(CMx):
        """Returns the proportion correctly classified"""
        correctClass = 0
        for i in range(len(CMx)) : correctClass = correctClass + CMx[i][i]
        total = sum(sum(CMx))
        return correctClass / float(total)
    CM = numpy.array(_CM)
    p_correctlyClassed = calcClassAccuracy(CM)
    measured = sum(CM)
    p_measured = numpy.array(map(lambda x : x/sum(measured), measured))
    predicted = sum(CM.T)
    p_predicted = numpy.array(map(lambda x : x/sum(predicted), predicted))
    prob_chance = sum(p_measured * p_predicted)
    return (p_correctlyClassed - prob_chance ) / (1 - prob_chance)

def Kappa(res=None):
    if res == None:
        return {"type":CLASSIFICATION}
    Kappa_s = []
    for cm in ConfMat(res):
        Kappa_s.append(calcKappa(cm))
    return Kappa_s

def generalCVconfMat(data, learners, nFolds = 5):
    """
    General method for printing the X fold CV confusion matrix of an Orange data set (data)
    with any number of classes. learners is a list of AZorange learners.
    """

    res = crossValidation(learners, data, stratified=orange.MakeRandomIndices.StratifiedIfPossible, folds = nFolds)
    classes = data.domain.classVar.values

    for idx in range(len(learners)):
        cm = orngStat.computeConfusionMatrices(res)[idx]
        print "Results for "+learners[idx].name
        print "\t"+"\t".join(classes)
        for className, classConfusions in zip(classes, cm):
            print ("%s" + ("\t%i" * len(classes))) % ((className, ) + tuple(classConfusions))

def getClassificationAccuracy(testData, classifier):
    #Construct the list of experimental and predicted values: [(exp1, pred1), (exp2, pred2), ...]
    if not len(testData):
        return 0.0
    exp_pred = []
    # Predict using bulk-predict
    predictions = classifier(testData)
    # Gather predictions 
    for n,ex in enumerate(testData):
        exp_pred.append( (str(ex.getclass()), str(predictions[n])) )
    return calcClassificationAccuracy(exp_pred)

def calcClassificationAccuracy(exp_pred_Val):
    correct = 0.0
    for val in exp_pred_Val:
        #print str(classifier(ex)) + "->" + str(ex.getclass())
        if val[0] == val[1]:
            correct = correct + 1.0
    ClassificationAccuracy = correct/len(exp_pred_Val)
    return ClassificationAccuracy


def getRMSE(testData, predictor):
    #Construct the list of experimental and predicted values: [(exp1, pred1), (exp2, pred2), ...]
    exp_pred = []
    for ex in testData:
        exp_pred.append( (ex.getclass(), predictor(ex)) )
    return calcRMSE(exp_pred)

def calcRMSE(exp_pred_Val):
    accSum = 0.0
    nPredEx = 0
    for idx,val in enumerate(exp_pred_Val):
        try:
            accSum = accSum + math.pow(val[0]-string.atof(str(val[1])),2)
            nPredEx = nPredEx + 1 
        except:
            if verbose > 0: print "Warning!!!!"
            if verbose > 0: print "No prediction could be made for the example idx = ",idx
            if verbose > 0: print val
    if not nPredEx:
        accuracy = 999999
    else:
        accuracy = math.sqrt(accSum/nPredEx)
    return accuracy


def getRsqrt(testData, predictor):
    """Calculate the coefficient of determination (R-squared) for the orange model predictor on the data set testData. 
        This uses the Test Set Activity Mean
        R^2 = 1 - sum((pred - actual)^2)/(sum((testMean - actual)^2))"""
        
    #Construct the list of experimental and predicted values: [(exp1, pred1), (exp2, pred2), ...]
    exp_pred = []
    for ex in testData:
        exp_pred.append( (ex.getclass(), predictor(ex)) )
    return calcRsqrt(exp_pred)

def calcRsqrt(exp_pred_Val):
    """Calculates the Rsqrt of the predicted values in exp_pred_Val[1] against the 
        respective experimental values in exp_pred_Val[0]         
        Input example:

        [ (ExperimentalValue1, PredictedValue1),        # In respect to 1st Ex
          (ExperimentalValue2, PredictedValue2),        # In respect to 2nd Ex
          (ExperimentalValue3, PredictedValue3),        # In respect to 3rd Ex
          (ExperimentalValue4, PredictedValue4),        # In respect to 4rd Ex
          ...                                           # ...
        ]
    """
    # Calc mean of the experimental response variable
    actualValuesList = []
    for val in exp_pred_Val:
        actualValuesList.append(val[0])
    testMean = statc.mean(actualValuesList)

    errSum = 0.0
    meanSum = 0.0
    for val in exp_pred_Val:
        errSum = errSum + math.pow(val[0] - string.atof(str(val[1])),2)
        meanSum = meanSum + math.pow(testMean - val[0],2)
    if not meanSum:
        Rsqrt = -999999
    else:
        Rsqrt = 1 - errSum/meanSum
    return Rsqrt


def calcMCC(CM):
    """ CM =   [[TP, FN],
                [FP, TN]]
    """
    #Compute MCC = (TP x TN - FP x FN) / sqrt( (TP + FP)(TP + FN)(TN + FP)(TN + FN) )
    if len(CM) != 2:
        print "WARNING: Cannot calculate MCC for other than binary classification" 
        return None   
    [TP, FN], [FP, TN] = map(None,CM)    
    sqrtArg = 1 
    for arg in [(TP + FP),(TP + FN),(TN + FP),(TN + FN)]:
        if arg != 0:    # According to the paper where MCC was defined, if one of the arguments is zero, assume it as 1
            sqrtArg *= arg
    MCC = (TP * TN - FP * FN) / math.sqrt(1.0 * sqrtArg)
    return MCC

def stability(res):
    mean = statc.mean(res)
    dists = [abs(x-mean) for x in res]
    return statc.mean(dists)
    

def getQ2(testData, predictor):
    """Calculate the predictive squared correlation coefficient Q2, which uses the Training Set Activity Mean.. 
        Q^2 = 1 - sum((pred - actual)^2)/(sum((trainMean - actual)^2))
        This is according:   
                Comments on the Definition of the Q2 Parameter for QSAR Validation
                Viviana Consonni, Davide Ballabio, Roberto Todeschini
                Journal of Chemical Information and Modeling 2009 49 (7), 1669-1678"""

    # Test if the predictor is compatible with getQ2
    if not testData.domain.classVar or testData.domain.classVar.varType != orange.VarTypes.Continuous:
        print "The dataset is not suitable for calculatinmg Q2. Data must have Continuous Class" 
        return None
    elif not hasattr(predictor,"basicStat") or not predictor.basicStat:
        print "Q2 Error: The predictor is not compatible with the use fo getQ2. It has no basicStat defined."
        return None
    # Calc average of the training class variable
    trainMean = predictor.basicStat[testData.domain.classVar.name]["avg"]

    errSum = 0.0
    meanSum = 0.0
    for ex in testData:
        errSum = errSum + math.pow(ex.getclass() - string.atof(str(predictor(ex))),2)
        meanSum = meanSum + math.pow(trainMean - ex.getclass(),2)

    if not meanSum:
        Q2 = -999999
    else:
        Q2 = 1 - errSum/meanSum
    return Q2


def Sensitivity(confMatrixList, classes):
##scPA  Added last line of next comment ##ecPA
    """
    Takes a orngStat.confusionMatrices output object with N classes and computes the sensitivity 
    for each class returned as a dictionary indexed by the class name.
    The return object is a list with the lenght of the number of confusion matrices in confMatrixList. 
    The dictionary holding the sensitivities constitutes the objects of the returned list. 
    Sensitivity is obtained by dividing the diagonal element by the row sum.
    If the row sum is 0, it sets the Sensitivity to "N/A"
    """
   
    sensitivityList = []
    for confMatrix in confMatrixList:
        sensitivityDict = {}
        # Loop over the rows of the confusion matrix
        for idx in range(len(classes)):
##scPA
            if sum(confMatrix[idx])==0:
                sensitivityDict[classes[idx]] = "N/A"
            else:        
##ecPA
                sensitivityDict[classes[idx]] = float(confMatrix[idx][idx])/float(sum(confMatrix[idx]))
        sensitivityList.append(sensitivityDict)

    #print "End sensitivity "+str(sensitivityList)
    return sensitivityList
        

def Predictivity(confMatrixList, classes):
##scPA  Added last line of next comment ##ecPA
    """
    Takes a orngStat.confusionMatrices output object with N classes and computes the sensitivity 
    for each class returned as a dictionary indexed by the class name.
    The return object is a list with the lenght of the number of confusion matrices in confMatrixList. 
    The dictionary holding the sensitivities constitutes the objects of the returned list. 
    Predictivity is obtained by dividing the diagonal element by the column sum of the confusion matrix.
    If one class was never predicted, the predictivity is set to "N/A"
    """

    PredictivityList = []
    for confMatrix in confMatrixList:
        PredictivityDict = {}
        # Loop over the rows of the confusion matrix
        for idx in range(len(classes)):
            colSum = 0
            # Loop over the columns of confMatrix 
            for innerIdx in range(len(classes)):
                colSum = colSum + confMatrix[innerIdx][idx]
##scPA
            if colSum==0:
                PredictivityDict[classes[idx]] = "N/A"
            else:
##ecPA
               PredictivityDict[classes[idx]] = float(confMatrix[idx][idx])/float(colSum)
        PredictivityList.append(PredictivityDict)

    #print "End Predictivity "+str(PredictivityList)
    return PredictivityList            


def AUConeVSall(results, values, AUCList):
    """Retrun a list of lists where each element is a dictionary with one element per class with the value AUC_single. 
       Uses the orngTest.ExperimentResults object and data.domain.classVar.values"""
    #AUCList = []
    # Loop over the results for each learner in results
    # This is a work around as AUC_single does not seem to work with multiple learners.
    for keepIdx in range(results.numberOfLearners):
        result = copy.deepcopy(results)
        # Remove all learners except keepIdx
        for idx in range(results.numberOfLearners):
            if idx != keepIdx: result.remove(idx)
        AUCdict = {}
        for value in values:
            # Uses own modified version of this function because of orange bug.
            if result.numberOfIterations > 1:
                AUCdict[value] = AUC_single(result, classIndex = values.index(value))[0]
            else:
                AUCdict[value] = AUC_single(result, classIndex = values.index(value))[0][0]
        AUCList.append([AUCdict])

    return AUCList


# Computes AUC; in multivalued class problem, AUC is computed as one against all
# Results over folds are averages; if some folds examples from one class only, the folds are merged
def AUC_single(res, classIndex = -1, useWeights = True):
    if classIndex<0:
        if res.baseClass>=0:
            classIndex = res.baseClass
        else:
            classIndex = 1

    if res.numberOfIterations > 1:
        return orngStat.AUC_iterations(orngStat.AUC_i, orngStat.splitByIterations(res), (classIndex, useWeights, res, res.numberOfIterations))
    else:
        return orngStat.AUC_i(res, classIndex, useWeights)
        #return AUC_i([res], classIndex, useWeights)

def Q2(res = None, trainMeans = None):
    """Calculate the predictive squared correlation coefficient Q2, which uses the Training Set Activity Mean.. 
        Q^2 = 1 - sum((pred - actual)^2)/(sum((trainMean - actual)^2))
        res will have n Learner predictions and trainMeans the mean of the class on the trainSet resectively to the n Learners
        This is according:   
                Comments on the Definition of the Q2 Parameter for QSAR Validation
                Viviana Consonni, Davide Ballabio, Roberto Todeschini
                Journal of Chemical Information and Modeling 2009 49 (7), 1669-1678"""
    if res == None:
        return {"type":REGRESSION}
    nLearners = len(res.results[0].classes)
    if trainMeans == None or len(trainMeans) != nLearners:
        print "Q2 ERROR: The train mean must be provided in order to calculate Q2"
        return None

    if res.numberOfIterations > 1:
        print "ERROR: Q2 does not support more than one iteration!"
        return None
    else:
        errSums = [0.0]*res.numberOfLearners
        meanSums = [0.0]*res.numberOfLearners
        for tex in res.results:
            errSums = map(lambda res, cls, ac = float(tex.actualClass):
                       res + (float(cls) - ac)**2, errSums, tex.classes)
            meanSums = map(lambda res, mean, ac = float(tex.actualClass):
                       mean and res + (ac - mean)**2 or 0.0, meanSums, trainMeans)

        Q2s =  [ x[1] and 1-(x[0]/x[1]) or None for x in zip(errSums, meanSums)]

    return [x!=None and round(x,3) or None for x in Q2s]


def R2(res = None):
    """
    Truncate the orange method to 3 decimals. Allow for no input arguments. Used by the optimizer.
    """
    if res == None:
        return {"type":REGRESSION}
    else:
        scores = orngStat.R2(res)    
        return [round(x,3) for x in scores]

def RMSE(res = None):
    """
    Truncate the orange method to 3 decimals. Allow for no input arguments. Used by the optimizer.
    """
    if res == None:
        return {"type":REGRESSION}
    else:
        scores = orngStat.RMSE(res)    
        return [round(x,3) for x in scores]

def CA(res = None):
    """
    Truncate the orange method to 3 decimals. Allow for no input arguments. Used by the optimizer.
    """
    if res == None:
        return {"type":CLASSIFICATION}
    else:
        scores = orngStat.CA(res)    
        return [round(x,3) for x in scores]



##scPA
def Rsqrt_obsolete(res = None):
    """
    Calculates the R-squared (Coefficient of determination) of orngTest.ExperimentResults in res
    The results res must be from a learner
    """
    # If Called without arguments, return the type of problems this method can be used for: 
    # 1 - Classification problems (Discrete Class)
    # 2 - Regression problems (Continuous Class)
    # 3 - Both Regression and Classification problems (Continuous or Discrete Class)
    if res == None:
        return {"type":REGRESSION}

    if res.numberOfIterations > 1:
        Rs = [[0.0] * res.numberOfIterations for i in range(res.numberOfLearners)]
        errSum = [[0.0] * res.numberOfIterations for i in range(res.numberOfLearners)]
        meanSum = [[0.0] * res.numberOfIterations for i in range(res.numberOfLearners)]
        means = [[0.0] * res.numberOfIterations for i in range(res.numberOfLearners)]
        nIter = [0]*res.numberOfIterations
        for tex in res.results:
            ac = float(tex.actualClass)
            nIter[tex.iterationNumber] += 1
            for i, cls in enumerate(tex.classes):
                means[i][tex.iterationNumber] += ac
        for nit, it in enumerate(nIter):
            for i, cls in enumerate(tex.classes):
                means[i][nit] /=it

        for tex in res.results:
            ac = float(tex.actualClass)
            for i, cls in enumerate(tex.classes):
                errSum[i][tex.iterationNumber] += (float(cls) - ac)**2
                meanSum[i][tex.iterationNumber] += (means[i][tex.iterationNumber] - ac)**2
        for learner in range(res.numberOfLearners):
            for it in range(len(nIter)):
                if meanSum[learner][it]==0:
                    return "N/A"
                Rs[learner][it] = 1-(errSum[learner][it] / meanSum[learner][it])
        return [statc.mean(x) for x in Rs]

    else:
        RsqrtList=[]
        for nLearner in range(len(res.results[0].classes)):
            # Calc average of the prediction variable
            testMean = 0
            for ex in res.results:
                testMean = testMean + ex.actualClass
            testMean = testMean/len(res.results)
            errSum = 0.0
            meanSum = 0.0
            for ex in res.results:
                errSum = errSum + math.pow(ex.actualClass - ex.classes[nLearner],2)
                meanSum = meanSum + math.pow(testMean - ex.actualClass,2)
            if meanSum==0:
                return "N/A"
            RsqrtList.append(1 - errSum/meanSum)
        return RsqrtList

def RMSE_obsolete(res = None):
    """
    Calculates the Root Mean Squared Error of orngTest.ExperimentResults in res
    The results res must be from a regressor
    """
    # If Called without arguments, return the type of problems this method can be used for: 
    # 1 - Classification problems (Discrete Class)
    # 2 - Regression problems (Continuous Class)
    # 3 - Both Regression and Classification problems (Continuous or Discrete Class)
    if res == None:
        return {"type":REGRESSION}

    if res.numberOfIterations > 1:
        MSEs = [[0.0] * res.numberOfIterations for i in range(res.numberOfLearners)]
        nIter = [0]*res.numberOfIterations
        for tex in res.results:
            ac = float(tex.actualClass)
            nIter[tex.iterationNumber] += 1
            for i, cls in enumerate(tex.classes):
                MSEs[i][tex.iterationNumber] += (float(cls) - ac)**2
        MSEs = [[x/ni for x, ni in zip(y, nIter)] for y in MSEs]
        MSEs = [[math.sqrt(x) for x in y] for y in MSEs]

        # Print output from each fold to tem file
        RMSEfoldList = MSEs
        RMSE = [statc.mean(x) for x in RMSEfoldList]
        RMSEstd = stats.stdev(RMSEfoldList[0])
        #print str(RMSE[0])+"\t"+str(RMSEstd)+"\t"+string.join( [str(x) for x in RMSEfoldList[0]] , "\t")

        return [round(statc.mean(x),2) for x in MSEs]

    else:
        MSEs = [0.0]*res.numberOfLearners
        for tex in res.results:
            MSEs = map(lambda res, cls, ac = float(tex.actualClass):
                       res + (float(cls) - ac)**2, MSEs, tex.classes)

        MSEs = [x/(len(res.results)) for x in MSEs]
        return [round(math.sqrt(x),2)  for x in MSEs]


def CA_obsolete(res = None, returnFoldStat = False):
    """
    Calculates the classification Accuracy of orngTest.ExperimentResults in res
    The results res must be from a classifier
    """
    # If Called without arguments, return the type of problems this method can be used for: 
    # 1 - Classification problems (Discrete Class)
    # 2 - Regression problems (Continuous Class)
    # 3 - Both Regression and Classification problems (Continuous or Discrete Class)
    if res == None:
        return {"type":CLASSIFICATION}

    if res.numberOfIterations > 1:
        CAs = [[0.0] * res.numberOfIterations for i in range(res.numberOfLearners)]
        nIter = [0]*res.numberOfIterations
        for tex in res.results:
            ac = tex.actualClass
            nIter[tex.iterationNumber] += 1
            for i, cls in enumerate(tex.classes):
                if cls == ac:
                    CAs[i][tex.iterationNumber] += 1
        CAs = [[x/ni for x, ni in zip(y, nIter)] for y in CAs]

        CAfoldList = CAs
        CA = [statc.mean(x) for x in CAs]
        CAstd = stats.stdev(CAfoldList[0])

        if returnFoldStat:
            return [round(statc.mean(x),3) for x in CAs], CAfoldList
        else:
            return [round(statc.mean(x),3) for x in CAs]

    else:
        CAs = [0.0]*res.numberOfLearners
        for tex in res.results:
            CAs = map(lambda res, cls, ac = tex.actualClass:
                       res + types.IntType(cls == ac), CAs, tex.classes)
        return [round(x/(len(res.results)),3) for x in CAs]


##ecPA

def getRMSEstd(res, nFolds):
    """
    Method for calculating the std of RMSE of nFolds in a crossvalidation (returned).
    res is the object containing the results from orngTest methods such as crossValidation.
    """

    # Initialize a list to contain lists of errors for each fold.
    errorList = []
    for idx in range(nFolds):
        errorList.append([])

    # ex contains info on the fold number, prediction and actural responses for exah example used in the CV
    # Append ex error to correct fold list
    for ex in res.results:
         error = (ex.classes[0]- ex.actualClass)**2
         errorList[ex.iterationNumber].append(error)

    # RMSE of the different folds
    RMSElist = []
    for idx in range(nFolds):
        average =  sum(errorList[idx])/len(errorList[idx])
        RMSElist.append(math.sqrt(average))
    RMSEstd = stats.stdev(RMSElist)
    RMSEmean = statc.mean(RMSElist)
    if verbose > 0: print str(RMSEmean)+"\t"+str(RMSEstd)+"\t"+string.join( [str(x) for x in RMSElist], "\t")
    return RMSEstd, RMSElist


def WilcoxonRankTest(accLearner1, accLearner2):
    """
    The input is two list with the value pairs to be compared!
    Single sided Wilcoxon rank sum test. 
    See critical values: http://www.euronet.nl/users/warnar/demostatistiek/tables/WILCOXONTABEL.htm
    http://web.anglia.ac.uk/numbers/biostatistics/wilcoxon/local_folder/critical_values.html
    """
    # Learner 1 is the most accurate
    diffPlus = []
    # Learner 2 is the most accurate
    diffMinus = []
    for idx in range(len(accLearner2)):
        diff = accLearner1[idx]-accLearner2[idx]
        if diff > 0:
            diffPlus.append(abs(diff))
        elif diff < 0:
            diffMinus.append(abs(diff))
        else:
            diffPlus.append(abs(diff))
            diffMinus.append(abs(diff))
    diffPlus.sort()
    diffMinus.sort()

    # Rank the differences according to absolute values
    # R is a dictionary indexed by the rank number and with the values +, - or +/-
    # indicating which learner the rank number will be assigned to
    # The greater the diff the greater the rank idx
    R = {}
    for idx in range(len(accLearner1)):
        # Get the smallest value in each diff list (small diff -> small idx)
        try: diffPlusMin = diffPlus[0]
        except: diffPlusMin = 10000  # No more diffPlus elements, always take diffMinus
        try: diffMinusMin = diffMinus[0]
        except: diffMinusMin = 10000
        if diffPlusMin < diffMinusMin:
            if len(diffPlus) > 0: min = diffPlus.pop(0)
            R[str(idx)] = "+"
        elif diffPlusMin == diffMinusMin:
            if len(diffPlus) > 0: min = diffPlus.pop(0)
            if len(diffMinus) > 0: min = diffMinus.pop(0)
            R[str(idx)] = "+/-"
        else:
            if len(diffMinus) > 0: min = diffMinus.pop(0)
            R[str(idx)] = "-"

    # Get rank sums for the two learners - The greater the sum, the more accurate the learner
    Rplus = 0
    Rminus = 0
    for key, value in R.iteritems():
        if value == "+":
            Rplus = Rplus + int(key)
        elif value == "-":
            Rminus = Rminus + int(key)
        elif value == "+/-":
            Rplus = Rplus + (1.0/2)*int(key)
            Rminus = Rminus + (1.0/2)*int(key)

    Rlist = [Rplus, Rminus]
    # Does not work!!
    #print min(Rlist)
    Rlist.sort()
    # ***** Already in Orange - don't use the above *************
    #T = Rlist.pop(0)
    T = statc.wilcoxont(accLearner1, accLearner2)[0]
    N = len(R)

    print "Rank sum of learner 1"
    print Rplus
    print "Rank sum of learner 2"
    print Rminus
    if Rplus < Rminus:
        print "The hypothesis is that learner 2 is the most accurate"
    else:
        print "The hypothesis is that learner 1 is the most accurate"

    info = "If the number of data sets (N) is equal to 16 (our regression suite):\n"
    info += "N " + str(N) +"\n"
    info += "If T < 35 there is a 10% chance that the hypothesis is not true\n"
    info += "If T < 29 there is a 5% chance that the hypothesis is not true\n"
    info += "T " + str(T) + "\n"

    info += "If the number of data sets (N) is equal to 17 (our classification suite):\n"
    info += "N " + str(N) +"\n"
    info += "If T < 41 there is a 10% chance that the hypothesis is not true\n"
    info += "If T < 34 there is a 5% chance that the hypothesis is not true\n"
    info += "T " + str(T) + "\n"
    # If N > 20
    #z = (T - (1.0/4)*N*(N+1))/math.sqrt((1.0/24)*N*(N+1)*(2*N+1))
    #print z
    print info

    #Return the index of the best LEarner
    if Rplus < Rminus:
        return (1, info)
    else:
        return (0, info)



from Orange.evaluation.testing  import Evaluation
import Orange
from Orange.misc import demangle_examples,getobjectname

def testOnData(models,testData, store_classifiers=False, store_examples=False):
        """ Makes used of Bulk-Predict"""
        evaluator = VarCtrlVal()

        test_results = orngTest.ExperimentResults(1,
                                        classifierNames = [getobjectname(l) for l in models],
                                        domain=testData.domain)#,
                                    #    test_type = test_type,
                                    #    weights=weight)
        test_results.classifiers = []
        if store_examples:
            test_results.examples = testData
        if store_classifiers:
            test_results.classifiers = models

        results = evaluator._test_on_data(models, testData, example_ids=None)
        test_results.results.extend(test_results.create_tested_example(0, example)
                                        for i, example in enumerate(testData))
        for nEx, nModel, res in results:
            test_results.results[nEx].set_result(nModel, *res)

        return test_results


def crossValidation(learners, data, folds=10,
            stratified=Orange.core.MakeRandomIndices.StratifiedIfPossible,
            preprocessors=(), random_generator=0, callback=None,
            store_classifiers=False, store_examples=False, testAttrFilter=None, testFilterVal=None):
    evaluator = VarCtrlVal()
    # Setting in advance the trainBias to be used
    examples = evaluator.getExamplesAndSetTrainBias(data, testAttrFilter, testFilterVal)

    # Proceeding with examples matching the test criterias
    return evaluator.cross_validation(learners, examples, folds,
            stratified, preprocessors, random_generator, callback,
            store_classifiers, store_examples)
        
def proportionTest(learners, data, learningProportion, times=10,
                   stratification=Orange.core.MakeRandomIndices.StratifiedIfPossible, preprocessors=(), randomGenerator=0,
                   callback=None, storeClassifiers=False, storeExamples=False,
                   testAttrFilter=None, testFilterVal=None):
    evaluator = VarCtrlVal()
    return evaluator.proportion_test(learners, data, learningProportion, times,
                   stratification, preprocessors, randomGenerator,
                   callback, storeClassifiers, storeExamples, testAttrFilter, testFilterVal)




class VarCtrlVal(Evaluation):
    trainBias = None # Exampels to be added everytime a train is performed! Should always be set using the getExamplesAndSetTrainBias method
    fixedIdx = None

    def getExamplesAndSetTrainBias(self, data, testAttrFilter, testFilterVal):
        """
        Collects and returns the examples that match the filterValue at the Attr defined
        The remaining examples (that do not match the filterValue at the Attr defined) are
        placed in the trainBias to be added in all train events.
        """
        self.trainBias = None
        if testAttrFilter is not None and  testFilterVal is not None and testAttrFilter in data.domain:
            if type(testFilterVal) != list:
                raise Exception("Invalid Attr filter value. It must be a list of strings")
            else:
                allDataEx = len(data)
                examples = orange.ExampleTable(data.domain)
                self.trainBias = orange.ExampleTable(data.domain)
                for ex in data:
                    inExamples = False
                    for Vfilter in testFilterVal:
                        if ex[testAttrFilter].value == Vfilter:
                            examples.append(ex)
                            inExamples = True
                            break
                    if not inExamples:
                        self.trainBias.append(ex)

                print "INFO: Variable control validation:"
                print "      Examples in data: "+str(allDataEx)
                print "      Examples selected for validation: "+str(len(examples))
                print "      Examples to be appended to the train set: "+str(len(self.trainBias))
                examples = dataUtilities.attributeDeselectionData(examples, [testAttrFilter])
        elif testAttrFilter is not None and testFilterVal is None and testAttrFilter in data.domain:
            #Enable pre-selected-indices
            self.fixedIdx = orange.LongList()
            allDataEx = len(data)
            examples = orange.ExampleTable(data.domain)
            self.trainBias = orange.ExampleTable(data.domain)
            foldsCounter = {}
            for ex in data:
                value = str(ex[testAttrFilter].value)
                if not miscUtilities.isNumber(value):
                   raise Exception("Invalid fold value:"+str(value)+". It must be str convertable to an int.")
                value = int(float(value))
                if value not in foldsCounter:
                    foldsCounter[value] = 1
                else:
                    foldsCounter[value] += 1
                if not miscUtilities.isNumber:
                    raise Exception("Invalid fold value:"+str(value)+". It must be str convertable to an int.")
                if value != 0:
                    examples.append(ex)
                    self.fixedIdx.append(value - 1)
                else:
                    self.trainBias.append(ex)

            print "INFO: Pre-selected "+str(len([f for f in foldsCounter if f != 0]))+" folds for CV:"
            print "      Examples in data: "+str(allDataEx)
            print "      Examples selected for validation: "+str(len(examples))
            print "      Examples to be appended to the train set: "+str(len(self.trainBias))
            examples = dataUtilities.attributeDeselectionData(examples, [testAttrFilter])

        else:
            examples = data

        return examples


    def one_fold_with_indices(self, learners, examples, fold, indices, preprocessors=(), weight=0):
        """Perform one fold of cross-validation like procedure using provided indices."""
        learn_set = examples.selectref(indices, fold, negate=1)
        test_set = examples.selectref(indices, fold, negate=0)
        if len(learn_set)==0 or len(test_set)==0:
            return (), ()

        # learning
        learn_set, test_set = self._preprocess_data(learn_set, test_set, preprocessors)
        #Add train bias to the lear_set
        if self.trainBias:
            learn_set = dataUtilities.concatenate([learn_set, self.trainBias], True)[0]
            
        if not learn_set:
            raise SystemError("no training examples after preprocessing")
        if not test_set:
            raise SystemError("no test examples after preprocessing")

        classifiers = [learner(learn_set, weight) for learner in learners]

        # testing
        testset_ids = (i for i, _ in enumerate(examples) if indices[i] == fold)
        results = self._test_on_data(classifiers, test_set, testset_ids)

        return results, classifiers
 

    def proportion_test(self, learners, data, learning_proportion, times=10,
                   stratification=Orange.core.MakeRandomIndices.StratifiedIfPossible, preprocessors=(), random_generator=0,
                   callback=None, store_classifiers=False, store_examples=False, testAttrFilter=None, testFilterVal=None):
        """
        Perform a test, where learners are trained and tested on different data sets. Training and test sets are
        generated by proportionally splitting data.

        :param learners: list of learners to be tested
        :param data: a dataset used for evaluation
        :param learning_proportion: proportion of examples to be used for training
        :param times: number of test repetitions
        :param stratification: use stratification when constructing train and test sets.
        :param preprocessors: a list of preprocessors to be used on data.
        :param callback: a function that is be called after each classifier is computed.
        :param store_classifiers: if True, classifiers will be accessible in test_results.
        :param store_examples: if True, examples will be accessible in test_results.
        :return: :obj:`ExperimentResults`
        """
        examples = self.getExamplesAndSetTrainBias(data, testAttrFilter, testFilterVal)

        pick = Orange.core.MakeRandomIndices2(stratified = stratification, p0 = learning_proportion, randomGenerator = random_generator)

        examples, weight = demangle_examples(examples)

        test_type = self.check_test_type(examples, learners)
        
        test_results = orngTest.ExperimentResults(times,
                                        classifierNames = [getobjectname(l) for l in learners],
                                        domain=examples.domain,
                                        test_type = test_type,
                                        weights=weight)
        test_results.classifiers = []
        offset=0
        for time in xrange(times):
            indices = pick(examples)
            learn_set = examples.selectref(indices, 0)
            test_set = examples.selectref(indices, 1)
            #Add train bias to the lear_set
            if self.trainBias:
                learn_set = dataUtilities.concatenate([learn_set, self.trainBias], True)[0]
            classifiers, results = self._learn_and_test_on_test_data(learners, learn_set, weight, test_set, preprocessors)
            if store_classifiers:
                test_results.classifiers.append(classifiers)

            test_results.results.extend(test_results.create_tested_example(time, example)
                                        for i, example in enumerate(test_set))
            for example, classifier, result in results:
                test_results.results[offset+example].set_result(classifier, *result)
            offset += len(test_set)

            if callback:
                callback()
        return test_results

    def cross_validation(self, learners, examples, folds=10,
            stratified=Orange.core.MakeRandomIndices.StratifiedIfPossible,
            preprocessors=(), random_generator=0, callback=None,
            store_classifiers=False, store_examples=False):
        """Perform cross validation with specified number of folds.

        :param learners: list of learners to be tested
        :param examples: data table on which the learners will be tested
        :param folds: number of folds to perform
        :param stratified: sets, whether indices should be stratified
        :param preprocessors: a list of preprocessors to be used on data.
        :param random_generator: random seed or random generator for selection
               of indices
        :param callback: a function that will be called after each fold is
               computed.
        :param store_classifiers: if True, classifiers will be accessible in
               test_results.
        :param store_examples: if True, examples will be accessible in
               test_results.
        :return: :obj:`ExperimentResults`
        """
        (examples, weight) = demangle_examples(examples)

        if self.fixedIdx:
            # ignore folds
            indices = self.fixedIdx
        else:
            indices = Orange.core.MakeRandomIndicesCV(examples, folds,
                stratified=stratified, random_generator=random_generator)

        return self.test_with_indices(
            learners=learners,
            examples=(examples, weight),
            indices=indices,
            preprocessors=preprocessors,
            callback=callback,
            store_classifiers=store_classifiers,
            store_examples=store_examples)



    def _test_on_data(self, classifiers, examples, example_ids=None):
        results = []

        if example_ids is None:
            numbered_examples = zip(range(len(examples)),examples)
        else:
            numbered_examples = zip(example_ids, examples) # itertools.izip(example_ids, examples)
        # For classifiers with _bulkPredict method, call with all examples at once
        bulkEnabledClassifiers = {}
        for c,model in enumerate(classifiers):
            if hasattr(model,"_bulkPredict"):
                bulkEnabledClassifiers[c] = {}
                testData = Orange.core.ExampleTable(examples[0].domain, [ex[1] for ex in numbered_examples])
                res = model(testData, Orange.core.GetBoth)
                for i, e in enumerate([ex[0] for ex in numbered_examples]):
                    bulkEnabledClassifiers[c][e] = copy.deepcopy(res[i])

        for e, example in numbered_examples:
            for c, classifier in enumerate(classifiers):
                if c in bulkEnabledClassifiers:
                    result = bulkEnabledClassifiers[c][e]
                else:
                    # Hide actual class to prevent cheating
                    ex2 = Orange.data.Instance(example)
                    if ex2.domain.class_var: ex2.setclass("?")
                    if ex2.domain.class_vars: ex2.set_classes(["?" for cv in ex2.domain.class_vars])
                    result = classifier(ex2, Orange.core.GetBoth)
                results.append((e, c, result))
        return results

