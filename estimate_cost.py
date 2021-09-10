import streamlit as st
import numpy as np

####Parameters
#Constant (Pi)
#Pi: Used for Wafer Area Calculation
Pi              = np.pi

##Fabrication Parameters
#Baseline Process Node
#Unit: [nm]
Baseline_Process= 5.0

##Wafer Parameters
#Price per Wafer
#Unit: [US Dollar]
Wafer_Price     = {'90':1650, '65':1937, '40':2274, '28':2891, '16':3984, '12':3984, '10':5992, '7':9346, '5':16988}

#Coefficient to Scale Die-Yield
#See H&P Book
#Unit: [N/A]
Scale_Die_Yield = 10.0

#Number of Defect Chips
#Unit: [Chips]
N_Defect        = 1


##Fabrication Parameters
#Test Cost per Chip
#Unit: [US Dollar]
Cost_Test       = 5

#Packaging Cost per Chip
#Unit: [US Dollar]
Cost_Package    = 2


##Market Parameters
#Average Price in Market
#Unit: [US Dollar]
Price_Market    = 10

#Number of Units Installed
#Unit: [Units]
N_installation  = 10000

#Market Share
#Unit:  [%]
Market_Share    = 5.0

#Sale Rate
#Unit:  [%]
Sale_Rate       = 85.0

#CAGR
#Unit:  [%]
CAGR            = 20.0

##NRE Cost
#Cost for Tool Software
#Unit: [K US Dollar]
Cost_Tools      = 300.0

#Salary for Engineer per Year
#Unit: [K US Dollar]
Engineer_Salary = 120.0

#Number of Engineers
#Units: [Persons]
Engineer_Workers= 10


st.sidebar.title('Cost Estimation')


##Market Parameters
st.subheader('Market Factors')
st.sidebar.subheader('Market Factors')
#Chip Price
price_market    = st.sidebar.slider('Chip Price in Market [US Dollar]', 100, Price_Market*500, Price_Market)
st.text('Chip Price in Market       [US Dollar] %s' % price_market)

#Number of Installations
number_of_installation = st.sidebar.slider('Installations in Market [Units]', 5000, N_installation*100, N_installation)
st.text('Installation in Market         [Units] %s' % number_of_installation)

#Market Volume
volume_market   = price_market * number_of_installation
st.text('Market Volume              [US Dollar] %s' % volume_market)

#Compound Average Growth Rate (CAGR: Prediction Number)
#Unit: [%]
#cagr            = st.sidebar.slider('Compound Average Growth Rate (CAGR) [%]', 2.0, 50.0, CAGR)
#st.text('CAGR                         [Percent] %s' % cagr)

market_share    = st.sidebar.slider('Market Share [%]', 0.0, 100.0, Market_Share)
st.text('Market Share                 [Percent] %s' % market_share)

#Sale Rate
sales_rate      = st.sidebar.slider('Sale Rate [%]', 0.0, 100.0, Sale_Rate)
st.text('Sale Rate                    [Percent] %s' % sales_rate)


##Semiconductor Fabrication Parameters
st.subheader('Semiconductor Factors')
st.sidebar.subheader('Semiconductor Factors')
#Wafer Diameter
wafer_diameter  = st.sidebar.selectbox(
                    'Wafer Diameter [mm]',
                    ('300', '200', '100'))
st.text('Wafer Diameter                    [mm] %s' % wafer_diameter)

#Wafer Area
#Unit: [mm**2]
wafer_area      = Pi * ((float(wafer_diameter))**2.0)/4.0
st.text('Wafer Area                     [mm**2] %s' % wafer_area)

#Estimating Process
#Unit:  [nm]
Process_Node = st.sidebar.selectbox("Process Node [nm]", ('90', '65', '40', '28', '16', '12', '10', '7', '5'))
estimating_process = int(Process_Node)

#Scale Die Yeld
die_yield_factor= st.sidebar.slider('Die Yield Factor', 1.0, 15.0, Scale_Die_Yield)
st.text('Die Yield Factor                       %s' % die_yield_factor)


##Design Factors
st.subheader('Design Factors')
st.sidebar.subheader('Design Factors')
#Design Transistors
#Unit:  [Transistors]
Num_Xtors       = st.sidebar.slider('Number of Million Transistors', 10.0, 65536.0, 10.0)
st.text('Number of Transistors  [M Transistors] %s' % Num_Xtors)

#Design Area
mim_space_factor= np.log(Num_Xtors) / 4.0
Space_Factor    = st.sidebar.slider('Space Factor [Transistors/Node]', 1.0/mim_space_factor, 1.0, 0.01)
space_factor    = 1.0 / Space_Factor
#Unit:  [mm**2]
#Transistors per Unit Area
Xtor_per_Area   = 1 / ((space_factor * estimating_process / 1000000) ** 2.0)

#Time to Production
month_for_design = st.sidebar.slider('Design Time [Months]', 0, 60, 8)
st.text('Desgin Time                   [Months] %s' % month_for_design)


###Fabrication Factors
st.subheader('Fabrication Factors')
st.sidebar.subheader('Fabrication Factors')
#Die Area
#Unit:  [mm**2]
Die_Area       = (Num_Xtors * 1000000.0) / Xtor_per_Area
st.text('Die Area                       [mm**2] %s' % Die_Area)

#Available Maximum Number of Chips before Yielding
#Unit:  [Chips]
negative_factor = (Pi * float(wafer_diameter)) / np.sqrt(2.0 * Pi * Die_Area)
num_chips       = int(np.floor((wafer_area/Die_Area - negative_factor)))
st.text('Max Dies/Wafer                  [Dies] %s' % num_chips)

defect_density  = st.sidebar.slider('Defect Density [Defects/mm**2]', 0.001, 90/estimating_process, 0.001)
st.text('Defect Density         [Defects/mm**2] %s' % defect_density)

#Number of Defect Chips
#Unit:  [Chips]
num_defect      = defect_density * Die_Area
st.text('Defect Dies/Wafer               [Dies] %s' % num_defect)

#Die Yield per Wafer
#Unit:  [%]
die_yield       = (num_chips - num_defect) / num_chips
st.text('Die Yield/Wafer           [Percentage] %s' % die_yield)

#Number of Available Chips after Yielding
#Unit:  [Chips]
N_Die_Yield     = int(np.floor(die_yield * num_chips))
st.text('Available Dies/Wafer            [Dies] %s' % N_Die_Yield)

#Number of Wafers needed for Target Market Share
#Unit:  [Wafers]
N_Wafer         = int(np.ceil((N_installation * market_share / 100.0) / N_Die_Yield))
st.text('Number of Wafers              [Wafers] %s' % N_Wafer)

#Wafer Price
#Unit:  [US Dollar]
wafer_price     = Wafer_Price[Process_Node]
st.text('Wafer Price                [US Dollar] %s' % wafer_price)

#Total Cost for Wafer
#Unit:  [US Dollar]
Cost_Total_Wafer= N_Wafer * wafer_price
st.text('Total Wafer Cost           [US Dollar] %s' % Cost_Total_Wafer)

#Die Cost
#Unit:  [US Dollar]
Die_Cost        = float(Cost_Total_Wafer) / float(N_Die_Yield)
st.text('Total Die Cost             [US Dollar] %s' % Die_Cost)


####NRE Cost Parameters
st.subheader('NRE Cost Factors')
st.sidebar.subheader('NRE Cost Factors')

#Cost for Tool
#Unit:  [K US Dollar]
cost_tools      = st.sidebar.slider('Tool Cost [K US Dollar]', 0, int(Cost_Tools*1.25), int(Cost_Tools))
st.text('Tool Cost                [K US Dollar] %s' % cost_tools)

#Number of Engineers
#Unit:  [Workers]
num_engineers   = st.sidebar.slider('Engineers', 5, 300, Engineer_Workers)
st.text('Number of Engineers                    %s' % num_engineers)

#Salary for Engineer per Year
#Unit: [K US Dollar]
engineer_salary = st.sidebar.slider('Engineer Salary [K US Dollar]', Engineer_Salary, Engineer_Salary*3, Engineer_Salary)
st.text('Engineer Salary Per Year [K US Dollar] %s' % engineer_salary)

#Worker Fees
#Fees per Year
#Unit: [K US Dollar]
Cost_Engineer   = num_engineers * engineer_salary
st.text('Total Salary             [K US Dollar] %s' % Cost_Engineer)

#Total NRE Cost per Year
#Unit: [K US Dollar]
Cost_NRE        = cost_tools + Cost_Engineer
st.text('Total NRE Cost/Year      [K US Dollar] %s' % (Cost_NRE))


####Total Cost
st.subheader('Total Cost')
#Total NRE Cost
#Unit: [K US Dollar]
Total_NRE_Cost = np.ceil(month_for_design / 12.0) * Cost_NRE
st.text('Total NRE Cost           [M US Dollar] %s' % (Total_NRE_Cost / 1000))

#Unit:  [M US Dollar]
Cost_Production = Die_Cost * number_of_installation * market_share * sales_rate
st.text('Production Cost          [M US Dollar] %s' % (Cost_Production / 1000000))

#Unit:  [M US Dollar]
Total_Cost      = Cost_Production + (Cost_Test + Cost_Package) * N_Die_Yield + (Total_NRE_Cost * 1000)
st.text('Total Cost to Production [M US Dollar] %s' % (Total_Cost / 1000000))

####Product
st.subheader('Profit')
Total_Profit    = (price_market * number_of_installation * market_share * sales_rate)
st.text('Total Profit             [M US Dollar] %s' % (Total_Profit / 1000000))
st.text('Profit-Cost Ratio        [Percentage]  %s' % ((Total_Profit - Total_Cost) / Total_Cost * 100))
Revenue         = Total_Profit- Total_Cost
st.text('Revenue                  [M US Dollar] %s' % (Revenue / 1000000))
