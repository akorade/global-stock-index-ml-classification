# Predicting Whether the Closing Price of NYSE Composite Index (NYA) will Increase or Decrease Based on Previous Days' Metrics
## Cohort: 8, Team: ML4

# Contents
- [Overview](#overview)  
- [Team Members / Roles and Responsibilities](#team-members--roles-and-responsibilities-week-1)
- [Business Objective](#business-objective)  
- [Details of Dataset](#details-of-dataset)  
- [Potential Risks and Uncertainties](#potential-risks-and-uncertainties)  
- [Methodology and Technology](#methodology-and-technology)   

# Overview 

This project seeks to develop a model that provides predictions on whether the closing price of the NYA will increase or decrease on the next trading day, based on the opening price, highest price, lowest price, adjusted close price, and trading volume from the previous trading day. 

# Team Members / Roles and Responsibilities (Week 1)
- Mahima Chhagani - Select, Train, and Evaluate Model Performance
- Jonah Eisen - Feature Engineering and Selection, Select, Train, and Evaluate Model Performance
- Ajinkya Korade - Exploratory Data Analysis, Select, Train, and Evaluate Model Performance
- Michelle Lin -  Project/Readme File Updates, Select, Train, and Evaluate Model Performance
- Deepan Munjal - Dataset Cleaning, and Preprocessing, Exploratory Data Analysis, Select, Train, and Evaluate Model Performance
- Smit Trivedi (TBD)

# Business Objective

Key Stakeholders:  Hedge fund managers that utilize futures trading in their strategies.

Why Hedge Funds? 
- Hedge fund are subject to fewer regulatory constraints than traditional investment pools. This enables it to take on strategies that are much riskier, including the use of derivatives (such as the trading of futures), borrowing heavily, or concentrating on a single sector. For funds that are so inclined, taking on more risk provides an opportunity for the fund to earn a greater return for its investors. The trade‑off is that losses can be large and rapid. The fund's managers are typically compensated with management fees and a share of the profits.

What is a Futures Contract? 
- A futures contract is the obligation to buy or sell an underlying asset at a fixed delivery price on a fixed delivery date. While the underlying asset of a futures contract can be a physical entity, such as precious metals, it can alternatively be a stock index, such as the S&P 500 and Nasdaq‑100. 
- A futures contract can be settled (1) by the buyer taking physical delivery of the asset or (2) via cash based on the difference between the contracted price and the final settlement price (either the buyer or seller will pay the difference depending on which party is in the money at the time). To reduce counterparty risk, futures contracts are "marked to market" daily, meaning the price differences are settled each day based on daily price fluctuations. 
- Because futures contracts are marked to market daily, to ensure the solvency of the parties, a margin account is required to trade (typically representing 3-12% of the contract's notional value). It essentially allows an investor to control a large position with little capital, relatively speaking (the investor pays the value of the futures contract + daily margin requirements instead of the value of the assets), which can significally amplify returns (or losses) due to high leverage.  
- Example: An investor buys a future of Index A, currently trading at 10,000 points. The exchange packages the future with a contract multiplier of $50 times the value of the index, meaning a single contract is worth $500,000. If Index A increases to 10,100 points the following day, the seller owes the buyer (10,100-10,000)(contract multiplier) = (100)($50) = $5,000. However, if Index A decreases to 9,500 points, the buyer owes the seller (10,000-9,500)(contract multiplier) = (500)($50) = $25,000. If the buyer opened the position with a 5% margin, or (0.05)($500,000) = $25,000, an increase of Index A from 10,000 to 10,100 points corresponds to a new contract value of $505,000, a 1% increase. However, the $5,000 gain corresponds to a 20% increase relative to $25,000 actually invested (excluding the price of the future). The 5% margin creates a leverage of 1/0.05 = 20:1.

Business Proposition:  The team believes that a model that performs reasonably well in predicting whether the price of the NYA will increase or decrease the next trading day will benefit hedge managers that seek to profit from higher risk futures trading strategies by capitalizing on daily price fluctuations of the futures positions held by the funds that they manage, as well as to manage potential liquidity needs of such funds due to potential margin calls. 

# Details of Dataset 

The dataset that the team is using contains daily price data for indices tracking stock exchanges from around the world, including the United States, Canada, Germany, Japan, China, etc. The data is available on Kaggle and is sourced from Yahoo! Finance by the data owner. The team has elected to use the indexProcessed.csv file as it essentially contains the same data as the original indexData.csv file but with null values removed and an extra column for closing prices converted to USD (for the exchanges that do not trade in USD). 

The indexProcessed.csv dataset contains 1 target variable (i.e., opening day price for the next trading day) and 8 feature variables (index name, date, highiest price, lowest price, closing price, adjusted closing price, trading volumne, and in USD).

After discussions, the team made certain preliminary decisions regarding data cleaning (based on what we know at Week 1): 
- The team will focus solely on the index prices for the NYSE Composite Index (NYA). The reason for this is that different stock exchanges have different seasonal trading patterns and use different weighting methodologies which may skew the data and lead to overfitting. 
- The team will remove data entries where the trading volume is 0 or where the opening price, high, low, and closing price are the same for that trading day. These entries seem to suggest that there were no trading activities happening on those particular days and hence may be unreliable for purposes of the model.  
- The team will use NYA stock exchange data from 2004-2021, which is expected to yield around 4300 data entries and should serve as a pretty good starting point for training and testing the model.  

# Potential Risks and Uncertainties 

(Team members to add additional points)

- Market prices are influenced by external factors such as economic conditions, human sentiiments, and new events, which will not be considered by the model when predicting outcome. 
- Even though the model may predict a decrease in the NYA index price the next day, the fund may benefit from holding the future position longer (instead of selling the position right away), if the overall expectation is for the index prices to go up in the near term (to avoid the cost of buying another futures contract).     
- Risk with ARIMAX Model - prices are often influenced by non-linear factors as referenced in point 1 above and the ARIMAX model uses linear assumptions. 
- Risk with Convolutional Neural Network Model - overfitting on noisy, non-stationary data. 

# Methodology and Technology  

## Methodology

(Team members to add additional points)

1. **Data Cleaning and Preprocessing**: Process of fixing or removing duplicate, incomplete/missing data within a dataset, as well as addressing outliers, and normalizing/scaling data. 

2. **Exploratory Data Analysis (EDA)**: Analyzing datasets (including using visualization methods) to understand their characteristics, the relationships between features, and identifying any patterns/assumptions.

3. **Feature Engineering and Selection**: Transforming raw data to create new informative features that aid/enhance the prediction accuracy of the model.  

4. **Select, Train, and Evaluate Model Performance**:
    - Choose appropriate algorithms to train and test the processed data. Choose one to act as the baseline model. 
    - Evaluate the models' performance using metrics such as accuracy, precision, reall, or RMSE. 
    - Compare the model(s) to the baseline model 

## Technology 

(Team members to add additional points)

- scikit-learn  
- Pandas and NumPy
- matplotlib
- TensorFlow
- Keras
- PyTorch

================================================================================================

## Week 1 Expectations (NTD: for guidance only, to remove at later date)

1. The business motivation for your project.
2. Which dataset you have chosen to use.
3. Risks or unknowns that you have identified.
4. How you
will approach the analysis.
5. Breakdown of roles/tasks assigned to each team member.

## Guiding Questions (General) (NTD: for guidance only, to remove at later date)

1. Who is the intended audience for your project?
2. What is the question you will answer with your analysis?
3. What are the key variables and attributes in your dataset?
4. Do you need to clean your data, and if so what is the best strategy?
5. How can you explore the relationships between different variables?
6. What types of patterns or trends are in your data?
7. Are there any specific libraries or frameworks that are well-suited to your project requirements?

## Machine Learning Guiding Questions (NTD: for guidance only, to remove at later date)
1. What are the specific objectives and success criteria for your machine learning model?
2. How can you select the most relevant features for training?
3. Are there any missing values or outliers that need to be addressed through preprocessing?
4. Which machine learning algorithms are suitable for the problem domain?
5. What techniques are available to validate and tune the hyperparameters?
6. How should the data be split into training, validation, and test sets?
7. Are there any ethical implications or biases associated with the machine learning model?
8. How can you document the machine learning pipeline and model architecture for future reference?
