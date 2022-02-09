import streamlit as st
import os
import pickle
import string
import webbrowser
import pandas as pd
import re

global detect_model
global detect_tfidf

st.title('Mutual Fund XBRLID Prdictions')

def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)

filename = file_selector()
st.write('You selected `%s`' % filename)

df = pd.read_csv(filename)
#st.write(df)

corpus = []
for x in df.Labels:
    if len(str(x)) > 3:
        corpus.append(re.sub(r'\b\d \d\d\b', '', x))
corpus = list(filter(None, corpus))



# with open('08022022tfidf.pickle' , 'rb') as f:
#     lr = pickle.load(f)
# with open('08022022model.pickle' , 'rb') as f:
#     lr = pickle.load(f)

open_file_tfidf = open('08022022tfidf.pickle' , 'rb')
detect_tfidf = pickle.load(open_file_tfidf)
open_file_tfidf.close()

open_file_model = open('08022022model.pickle' , 'rb')
detect_model = pickle.load(open_file_model)
open_file_model.close()

id_to_category = {0: 'rr_RiskReturnHeading',
 1: 'rr_ShareholderFeesCaption',
 2: 'rr_MaximumSalesChargeImposedOnPurchasesOverOfferingPrice',
 3: 'rr_MaximumDeferredSalesChargeOverOfferingPrice',
 4: 'rr_OperatingExpensesCaption',
 5: 'rr_ManagementFeesOverAssets',
 6: 'rr_OtherExpensesOverAssets',
 7: 'rr_ExpensesOverAssets',
 8: 'rr_NetExpensesOverAssets',
 9: 'rr_ExpenseExampleYear01',
 10: 'rr_ExpenseExampleYear03',
 11: 'rr_ExpenseExampleYear05',
 12: 'rr_ExpenseExampleYear10',
 13: 'rr_FeeWaiverOrReimbursementOverAssets',
 14: 'rr_Component1OtherExpensesOverAssets',
 15: 'rr_Component2OtherExpensesOverAssets',
 16: 'rr_Component3OtherExpensesOverAssets',
 17: 'rr_AcquiredFundFeesAndExpensesOverAssets',
 18: 'rr_LowestQuarterlyReturnLabel',
 19: 'rr_AverageAnnualReturnYear01',
 20: 'rr_AverageAnnualReturnYear05',
 21: 'rr_AverageAnnualReturnYear10',
 22: 'rr_AverageAnnualReturnSinceInception',
 23: 'rr_AverageAnnualReturnInceptionDate',
 24: 'rr_MoneyMarketSevenDayYield',
 25: 'rr_OtherExpensesNewFundBasedOnEstimates',
 26: 'rr_ExpenseExampleByYearCaption',
 27: 'rr_ShareholderFeeOther',
 28: 'rr_HighestQuarterlyReturnLabel',
 29: 'rr_BarChartLowestQuarterlyReturn',
 30: 'rr_YearToDateReturnLabel',
 31: 'rr_AverageAnnualReturnLabel',
 32: 'rr_ExpensesRestatedToReflectCurrent',
 33: 'rr_ExpensesNotCorrelatedToRatioDueToAcquiredFundFees',
 34: 'rr_BarChartHeading',
 35: 'rr_PerformanceTableHeading',
 36: 'rr_BarChartLowestQuarterlyReturnDate',
 37: 'rr_RedemptionFeeOverRedemption',
 38: 'rr_RiskNondiversifiedStatus',
 39: 'rr_ExpenseExampleNoRedemptionYear01',
 40: 'rr_ExpenseExampleNoRedemptionYear03',
 41: 'rr_ExpenseExampleNoRedemptionYear05',
 42: 'rr_ExpenseExampleNoRedemptionYear10',
 43: 'rr_MaximumSalesChargeOnReinvestedDividendsAndDistributionsOverOther',
 44: 'rr_MaximumAccountFee',
 45: 'rr_ExchangeFeeOverRedemption',
 46: 'rr_MaximumDeferredSalesChargeOverOther',
 47: 'rr_ExpenseExampleNoRedemptionByYearCaption',
 48: 'rr_DistributionAndService12b1FeesOverAssets',
 49: 'rr_AverageAnnualReturnCaption',
 50: 'rr_IndexNoDeductionForFeesExpensesTaxes',
 51: 'rr_ExpenseExampleHeading',
 52: 'rr_BarChartHighestQuarterlyReturn',
 53: 'rr_BarChartHighestQuarterlyReturnDate',
 54: 'rr_RedemptionFee',
 55: 'rr_MaximumCumulativeSalesChargeOverOfferingPrice',
 56: 'rr_PerformanceTableMarketIndexChanged',
 57: 'rr_PerformanceTableOneClassOfAfterTaxShown',
 58: 'rr_MaximumCumulativeSalesChargeOverOther',
 59: 'rr_FeeWaiverOrReimbursementOverAssetsDateOfTermination',
 60: 'rr_PerformanceTableUsesHighestFederalRate',
 61: 'rr_ExpensesRepresentBothMasterAndFeeder',
 62: 'rr_PerformanceTableNotRelevantToTaxDeferred',
 63: 'rr_ObjectiveHeading',
 64: 'rr_ExpenseHeading',
 65: 'rr_StrategyHeading',
 66: 'rr_RiskHeading',
 67: 'rr_BarChartAndPerformanceTableHeading',
 68: 'rr_PerformanceTableExplanationAfterTaxHigher',
 69: 'rr_PerformanceAdditionalMarketIndex',
 70: 'rr_AcquiredFundFeesAndExpensesBasedOnEstimates',
 71: 'rr_BarChartYearToDateReturnDate',
 72: 'rr_PortfolioTurnoverRate',
 73: 'rr_PerformanceTableDoesReflectSalesLoads'}


button_clicked = st.button("Show Result")
text_features = detect_tfidf.transform(corpus) # List of Input values
predictions = detect_model.predict(text_features)
if button_clicked:
    for text, predicted in zip(corpus, predictions):
        st.text(text)
        st.subheader(id_to_category[predicted])
