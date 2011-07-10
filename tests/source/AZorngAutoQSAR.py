import unittest
import os
import time

from AZutilities import dataUtilities
import AZorngTestUtil
from AZutilities import AutoQSAR
import AZOrangeConfig as AZOC


class evalUtilitiesTest(unittest.TestCase):

    def setUp(self):

        trainDataPath1 = os.path.join(AZOC.AZORANGEHOME,"tests/source/data/phosphoTop10Train.tab")
        trainDataPath2 = os.path.join(AZOC.AZORANGEHOME,"tests/source/data/iris.tab")
        trainDataPath3 = os.path.join(AZOC.AZORANGEHOME,"tests/source/data/Reg_No_metas_Test.tab")

        self.trainClass2 = dataUtilities.DataTable(trainDataPath1)
        self.trainClass3 = dataUtilities.DataTable(trainDataPath2)
        self.trainReg = dataUtilities.DataTable(trainDataPath3)


    def no_test_MLStatistics_Class2(self):
        MLStatistics = AutoQSAR.getMLStatistics(self.trainClass2)
        print MLStatistics

    def no_test_MLStatistics_Class3(self):
        MLStatistics = AutoQSAR.getMLStatistics(self.trainClass3)
        print MLStatistics

    def no_test_MLStatistics_Reg(self):
        MLStatistics = AutoQSAR.getMLStatistics(self.trainReg)
        print MLStatistics

    def no_test_selectModel(self):
        # returned by running AutoQSAR.getMLStatistics(...)
        MLstat_class2 = {'PLS': {'R2': None, 'CM': [[92.0, 8.0], [6.0, 44.0]], 'RMSE': None, 'CA': 0.90666666666666684, 'MCC': 0.7924288517503274, 'foldStat': {'CA': [0.93333333333333335, 0.8666666666666667, 0.8666666666666667, 0.8666666666666667, 0.93333333333333335, 0.8666666666666667, 0.93333333333333335, 1.0, 0.8666666666666667, 0.93333333333333335], 'MCC': [0.7924288517503274, 0.72222222222222221, 0.7385489458759964, 0.42307692307692307, 0.875, 0.70710678118654746, 0.82915619758884995, 1.0, 0.75592894601845451, 0.8660254037844386], 'CM': [[[92.0, 8.0], [6.0, 44.0]], [[8.0, 1.0], [1.0, 5.0]], [[9.0, 0.0], [2.0, 4.0]], [[12.0, 1.0], [1.0, 1.0]], [[7.0, 1.0], [0.0, 7.0]], [[10.0, 2.0], [0.0, 3.0]], [[11.0, 1.0], [0.0, 3.0]], [[8.0, 0.0], [0.0, 7.0]], [[8.0, 0.0], [2.0, 5.0]], [[9.0, 1.0], [0.0, 5.0]]], 'R2': None, 'RMSE': None}, 'StabilityValue': 0.039999999999999994}, 'CvBoost': {'R2': None, 'CM': [[96.0, 4.0], [3.0, 47.0]], 'RMSE': None, 'CA': 0.95333333333333337, 'MCC': 0.89562215103979814, 'foldStat': {'CA': [0.93333333333333335, 0.8666666666666667, 1.0, 0.93333333333333335, 1.0, 0.8666666666666667, 1.0, 1.0, 0.93333333333333335, 1.0], 'MCC': [0.89562215103979814, 0.72222222222222221, 1.0, 0.68138514386924687, 1.0, 0.70710678118654746, 1.0, 1.0, 0.87287156094396945, 1.0], 'CM': [[[96.0, 4.0], [3.0, 47.0]], [[8.0, 1.0], [1.0, 5.0]], [[9.0, 0.0], [0.0, 6.0]], [[13.0, 0.0], [1.0, 1.0]], [[8.0, 0.0], [0.0, 7.0]], [[10.0, 2.0], [0.0, 3.0]], [[12.0, 0.0], [0.0, 3.0]], [[8.0, 0.0], [0.0, 7.0]], [[8.0, 0.0], [1.0, 6.0]], [[10.0, 0.0], [0.0, 5.0]]], 'R2': None, 'RMSE': None}, 'StabilityValue': 0.046666666666666655}, 'CvSVM': {'R2': None, 'CM': [[97.0, 3.0], [2.0, 48.0]], 'RMSE': None, 'CA': 0.96666666666666679, 'MCC': 0.92547622274112473, 'foldStat': {'CA': [0.93333333333333335, 0.80000000000000004, 1.0, 1.0, 1.0, 0.93333333333333335, 1.0, 1.0, 1.0, 1.0], 'MCC': [0.92547622274112473, 0.57735026918962573, 1.0, 1.0, 1.0, 0.82915619758884995, 1.0, 1.0, 1.0, 1.0], 'CM': [[[97.0, 3.0], [2.0, 48.0]], [[8.0, 1.0], [2.0, 4.0]], [[9.0, 0.0], [0.0, 6.0]], [[13.0, 0.0], [0.0, 2.0]], [[8.0, 0.0], [0.0, 7.0]], [[11.0, 1.0], [0.0, 3.0]], [[12.0, 0.0], [0.0, 3.0]], [[8.0, 0.0], [0.0, 7.0]], [[8.0, 0.0], [0.0, 7.0]], [[10.0, 0.0], [0.0, 5.0]]], 'R2': None, 'RMSE': None}, 'StabilityValue': 0.046666666666666655}, 'CvANN': {'R2': None, 'CM': [[94.0, 6.0], [3.0, 47.0]], 'RMSE': None, 'CA': 0.94000000000000006, 'MCC': 0.86784841052179451, 'foldStat': {'CA': [0.93333333333333335, 0.8666666666666667, 0.93333333333333335, 0.80000000000000004, 0.93333333333333335, 0.93333333333333335, 1.0, 1.0, 1.0, 1.0], 'MCC': [0.86784841052179451, 0.72222222222222221, 0.8660254037844386, 0.29417420270727601, 0.875, 0.82915619758884995, 1.0, 1.0, 1.0, 1.0], 'CM': [[[94.0, 6.0], [3.0, 47.0]], [[8.0, 1.0], [1.0, 5.0]], [[9.0, 0.0], [1.0, 5.0]], [[11.0, 2.0], [1.0, 1.0]], [[7.0, 1.0], [0.0, 7.0]], [[11.0, 1.0], [0.0, 3.0]], [[12.0, 0.0], [0.0, 3.0]], [[8.0, 0.0], [0.0, 7.0]], [[8.0, 0.0], [0.0, 7.0]], [[10.0, 0.0], [0.0, 5.0]]], 'R2': None, 'RMSE': None}, 'StabilityValue': 0.048000000000000001}, 'CvRF': {'R2': None, 'CM': [[96.0, 4.0], [2.0, 48.0]], 'RMSE': None, 'CA': 0.96000000000000019, 'MCC': 0.91129317951287647, 'foldStat': {'CA': [0.93333333333333335, 0.8666666666666667, 1.0, 0.93333333333333335, 1.0, 0.93333333333333335, 1.0, 1.0, 1.0, 0.93333333333333335], 'MCC': [0.91129317951287647, 0.72222222222222221, 1.0, 0.68138514386924687, 1.0, 0.82915619758884995, 1.0, 1.0, 1.0, 0.8660254037844386], 'CM': [[[96.0, 4.0], [2.0, 48.0]], [[8.0, 1.0], [1.0, 5.0]], [[9.0, 0.0], [0.0, 6.0]], [[13.0, 0.0], [1.0, 1.0]], [[8.0, 0.0], [0.0, 7.0]], [[11.0, 1.0], [0.0, 3.0]], [[12.0, 0.0], [0.0, 3.0]], [[8.0, 0.0], [0.0, 7.0]], [[8.0, 0.0], [0.0, 7.0]], [[9.0, 1.0], [0.0, 5.0]]], 'R2': None, 'RMSE': None}, 'StabilityValue': 0.039999999999999994}}
        MLstat_class3 = {'PLS': {'R2': None, 'CM': [[50.0, 0.0, 0.0], [0.0, 47.0, 3.0], [0.0, 3.0, 47.0]], 'RMSE': None, 'CA': 0.96000000000000019, 'MCC': None, 'foldStat': {'CA': [0.93333333333333335, 0.8666666666666667, 0.93333333333333335, 0.93333333333333335, 1.0, 0.93333333333333335, 1.0, 1.0, 1.0, 1.0], 'MCC': [None, None, None, None, None, None, None, None, None, None], 'CM': [[[50.0, 0.0, 0.0], [0.0, 47.0, 3.0], [0.0, 3.0, 47.0]], [[5.0, 0.0, 0.0], [0.0, 3.0, 1.0], [0.0, 1.0, 5.0]], [[8.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 1.0, 5.0]], [[4.0, 0.0, 0.0], [0.0, 9.0, 0.0], [0.0, 1.0, 1.0]], [[3.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 7.0]], [[4.0, 0.0, 0.0], [0.0, 7.0, 1.0], [0.0, 0.0, 3.0]], [[5.0, 0.0, 0.0], [0.0, 7.0, 0.0], [0.0, 0.0, 3.0]], [[3.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 7.0]], [[6.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 7.0]], [[5.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 5.0]]], 'R2': None, 'RMSE': None}, 'StabilityValue': 0.039999999999999994}, 'CvSVM': {'R2': None, 'CM': [[50.0, 0.0, 0.0], [0.0, 47.0, 3.0], [0.0, 1.0, 49.0]], 'RMSE': None, 'CA': 0.97333333333333338, 'MCC': None, 'foldStat': {'CA': [0.93333333333333335, 0.8666666666666667, 1.0, 1.0, 1.0, 0.93333333333333335, 1.0, 1.0, 1.0, 1.0], 'MCC': [None, None, None, None, None, None, None, None, None, None], 'CM': [[[50.0, 0.0, 0.0], [0.0, 47.0, 3.0], [0.0, 1.0, 49.0]], [[5.0, 0.0, 0.0], [0.0, 3.0, 1.0], [0.0, 1.0, 5.0]], [[8.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 6.0]], [[4.0, 0.0, 0.0], [0.0, 9.0, 0.0], [0.0, 0.0, 2.0]], [[3.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 7.0]], [[4.0, 0.0, 0.0], [0.0, 7.0, 1.0], [0.0, 0.0, 3.0]], [[5.0, 0.0, 0.0], [0.0, 7.0, 0.0], [0.0, 0.0, 3.0]], [[3.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 7.0]], [[6.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 7.0]], [[5.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 5.0]]], 'R2': None, 'RMSE': None}, 'StabilityValue': 0.037333333333333309}, 'CvANN': {'R2': None, 'CM': [[49.0, 1.0, 0.0], [0.0, 47.0, 3.0], [0.0, 4.0, 46.0]], 'RMSE': None, 'CA': 0.94666666666666666, 'MCC': None, 'foldStat': {'CA': [0.93333333333333335, 0.8666666666666667, 0.8666666666666667, 0.93333333333333335, 1.0, 0.93333333333333335, 1.0, 1.0, 0.93333333333333335, 1.0], 'MCC': [None, None, None, None, None, None, None, None, None, None], 'CM': [[[49.0, 1.0, 0.0], [0.0, 47.0, 3.0], [0.0, 4.0, 46.0]], [[5.0, 0.0, 0.0], [0.0, 3.0, 1.0], [0.0, 1.0, 5.0]], [[7.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 1.0, 5.0]], [[4.0, 0.0, 0.0], [0.0, 9.0, 0.0], [0.0, 1.0, 1.0]], [[3.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 7.0]], [[4.0, 0.0, 0.0], [0.0, 7.0, 1.0], [0.0, 0.0, 3.0]], [[5.0, 0.0, 0.0], [0.0, 7.0, 0.0], [0.0, 0.0, 3.0]], [[3.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 7.0]], [[6.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 1.0, 6.0]], [[5.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 5.0]]], 'R2': None, 'RMSE': None}, 'StabilityValue': 0.042666666666666651}, 'CvRF': {'R2': None, 'CM': [[50.0, 0.0, 0.0], [0.0, 47.0, 3.0], [0.0, 2.0, 48.0]], 'RMSE': None, 'CA': 0.96666666666666679, 'MCC': None, 'foldStat': {'CA': [0.93333333333333335, 0.8666666666666667, 1.0, 0.93333333333333335, 1.0, 0.93333333333333335, 1.0, 1.0, 1.0, 1.0], 'MCC': [None, None, None, None, None, None, None, None, None, None], 'CM': [[[50.0, 0.0, 0.0], [0.0, 47.0, 3.0], [0.0, 2.0, 48.0]], [[5.0, 0.0, 0.0], [0.0, 3.0, 1.0], [0.0, 1.0, 5.0]], [[8.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 6.0]], [[4.0, 0.0, 0.0], [0.0, 9.0, 0.0], [0.0, 1.0, 1.0]], [[3.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 7.0]], [[4.0, 0.0, 0.0], [0.0, 7.0, 1.0], [0.0, 0.0, 3.0]], [[5.0, 0.0, 0.0], [0.0, 7.0, 0.0], [0.0, 0.0, 3.0]], [[3.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 7.0]], [[6.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 7.0]], [[5.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 5.0]]], 'R2': None, 'RMSE': None}, 'StabilityValue': 0.039999999999999994}}
        MLstat_reg = {'PLS': {'R2': 0.026754964703230688, 'CM': None, 'RMSE': 2.9031710044606367, 'CA': None, 'MCC': None, 'foldStat': {'CA': None, 'MCC': None, 'CM': None, 'R2': [-0.090421965091209255, -0.00028274731168198564, -0.006352921561681546, -0.030637288204948376, -0.13010222610838218, 0.056246757533533587, 0.11061589360315549, -0.078050837361554271, 0.052633378580207335, 0.095222601561329445], 'RMSE': [2.6128922579108145, 2.6683410813733679, 2.1213668049932441, 3.293503210440841, 3.1250291604189657, 2.9670549023910038, 3.0567026225727423, 3.1156839474738511, 2.8920001331800904, 3.0009338569733699]}, 'StabilityValue': 0.065000112229431944}, 'CvSVM': {'R2': -0.042209564080492035, 'CM': None, 'RMSE': 3.004270589947494, 'CA': None, 'MCC': None, 'foldStat': {'CA': None, 'MCC': None, 'CM': None, 'R2': [-0.27951576751643947, -0.11239175275116686, -0.35834437073366865, -0.012344144551545755, -0.03067350965971527, -0.012705058485049658, -0.0011490368323769928, -0.093894586327306628, -0.0076820238587205214, -0.0028044062589502872], 'RMSE': [2.8303948639519847, 2.8139011285390065, 2.4645949628312809, 3.2641435752165111, 2.9843913048625219, 3.0735327411326021, 3.2430815866690237, 3.1384955169060613, 2.98264128282413, 3.1593203759549655]}, 'StabilityValue': 0.095908922907721114}, 'CvANN': {'R2': -0.0040538034322801231, 'CM': None, 'RMSE': 2.9487639740786342, 'CA': None, 'MCC': None, 'foldStat': {'CA': None, 'MCC': None, 'CM': None, 'R2': [-0.43143614286013587, 0.02852823271395355, -0.06279848988582537, -0.034323006649574328, -0.12492256608717489, -0.032817197549909638, 0.13367476379849763, -0.12023982324901406, 0.061414340458295635, 0.13534319579718279], 'RMSE': [2.9937132243561368, 2.6296324196615206, 2.1800481067614346, 3.2993869933982509, 3.1178593760928237, 3.1039025992769882, 3.0168171640719259, 3.1760642528129446, 2.8785662307464159, 2.9336441530805319]}, 'StabilityValue': 0.11207326893533368}, 'CvRF': {'R2': 0.036567993086957351, 'CM': None, 'RMSE': 2.8884978878846694, 'CA': None, 'MCC': None, 'foldStat': {'CA': None, 'MCC': None, 'CM': None, 'R2': [-0.17731151201284168, -0.030991494786439144, -0.10756460102123766, 0.09011143846891867, -0.0029682405538629109, -0.013435898143151492, 0.096954338029730969, 0.010798998435165963, 0.065595415729422291, 0.052481063462476385], 'RMSE': [2.7150004242356105, 2.7089905793633657, 2.2254874332161116, 3.0945625702089345, 2.9440067374033778, 3.0746415805128628, 3.0800896886373059, 2.9845306949272428, 2.8721475648522383, 3.0709977682061966]}, 'StabilityValue': 0.064821300064324711}}

        
        selMLMethod = AutoQSAR.selectModel(self.trainClass2, MLstat_class2)
        print selMLMethod

        selMLMethod = AutoQSAR.selectModel(self.trainClass3,MLstat_class3)
        print selMLMethod

        selMLMethod = AutoQSAR.selectModel(self.trainReg, MLstat_reg)
        print selMLMethod


    def no_test_buildModel(self):
        MLMethod_class2 = {'MLMethod': 'CvSVM', 'CM': [[97.0, 3.0], [2.0, 48.0]], 'R2': None, 'RMSE': None, 'CA': 0.96666666666666679, 'MCC': 0.92547622274112473, 'StabilityValue': 0.046666666666666655, 'foldStat': {'CA': [0.93333333333333335, 0.80000000000000004, 1.0, 1.0, 1.0, 0.93333333333333335, 1.0, 1.0, 1.0, 1.0], 'MCC': [0.92547622274112473, 0.57735026918962573, 1.0, 1.0, 1.0, 0.82915619758884995, 1.0, 1.0, 1.0, 1.0], 'R2': None, 'CM': [[[97.0, 3.0], [2.0, 48.0]], [[8.0, 1.0], [2.0, 4.0]], [[9.0, 0.0], [0.0, 6.0]], [[13.0, 0.0], [0.0, 2.0]], [[8.0, 0.0], [0.0, 7.0]], [[11.0, 1.0], [0.0, 3.0]], [[12.0, 0.0], [0.0, 3.0]], [[8.0, 0.0], [0.0, 7.0]], [[8.0, 0.0], [0.0, 7.0]], [[10.0, 0.0], [0.0, 5.0]]], 'RMSE': None}}
        MLMethod_class3 = {'MLMethod': 'CvSVM', 'CM': [[50.0, 0.0, 0.0], [0.0, 47.0, 3.0], [0.0, 1.0, 49.0]], 'R2': None, 'RMSE': None, 'CA': 0.97333333333333338, 'MCC': None, 'StabilityValue': 0.037333333333333309, 'foldStat': {'CA': [0.93333333333333335, 0.8666666666666667, 1.0, 1.0, 1.0, 0.93333333333333335, 1.0, 1.0, 1.0, 1.0], 'MCC': [None, None, None, None, None, None, None, None, None, None], 'R2': None, 'CM': [[[50.0, 0.0, 0.0], [0.0, 47.0, 3.0], [0.0, 1.0, 49.0]], [[5.0, 0.0, 0.0], [0.0, 3.0, 1.0], [0.0, 1.0, 5.0]], [[8.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 6.0]], [[4.0, 0.0, 0.0], [0.0, 9.0, 0.0], [0.0, 0.0, 2.0]], [[3.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 7.0]], [[4.0, 0.0, 0.0], [0.0, 7.0, 1.0], [0.0, 0.0, 3.0]], [[5.0, 0.0, 0.0], [0.0, 7.0, 0.0], [0.0, 0.0, 3.0]], [[3.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 7.0]], [[6.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 7.0]], [[5.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 5.0]]], 'RMSE': None}}
        MLMethod_Reg = {'MLMethod': 'CvRF', 'CM': None, 'R2': 0.036567993086957351, 'RMSE': 2.8884978878846694, 'CA': None, 'MCC': None, 'StabilityValue': 0.064821300064324711, 'foldStat': {'CA': None, 'MCC': None, 'R2': [-0.17731151201284168, -0.030991494786439144, -0.10756460102123766, 0.09011143846891867, -0.0029682405538629109, -0.013435898143151492, 0.096954338029730969, 0.010798998435165963, 0.065595415729422291, 0.052481063462476385], 'CM': None, 'RMSE': [2.7150004242356105, 2.7089905793633657, 2.2254874332161116, 3.0945625702089345, 2.9440067374033778, 3.0746415805128628, 3.0800896886373059, 2.9845306949272428, 2.8721475648522383, 3.0709977682061966]}}
        
        model = AutoQSAR.buildModel(self.trainClass2, MLMethod_class2)
        print model

        model = AutoQSAR.buildModel(self.trainClass3, MLMethod_class3)
        print model

        model = AutoQSAR.buildModel(self.trainReg, MLMethod_Reg)
        print model


    def test_getModel2(self):
        model = AutoQSAR.getModel(self.trainClass2, savePath = "./MLStat_Bin.txt")
        print model
    def no_test_getModel(self):
        model = AutoQSAR.getModel(self.trainClass3)
        print model
    def test_getModelReg(self):
        model = AutoQSAR.getModel(self.trainReg, savePath = "./MLStat_Reg.txt")
        print model
 

        
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(evalUtilitiesTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    #unittest.main()

