#----------------------------------- Importing Libraries -----------------------------------#
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.io as pio
import plotly.express as px
import psycopg2
from PIL import Image
#--------------------------------------------------------------------------------------------#

#---------------- Custom Functions ----------------------------------------------------------#

# Custom Function to set the css for different components
def set_css():
    # Define the custom CSS
    styles = """
        <style>

            .stApp{
              background-color: #270C34;
              color: 	#FFFFFF !important;
              font: 15px;
            }    
   
            [data-testid="stHeader"] {
                background-color: #3E1C4D;
                color: white;
                padding: 10px;
                display: flex;
                align-items: flex-start;
            }

            [data-testid="stSidebar"] {
                background-color: #0B030F !important;
                color: 	#FFFFFF !important;
            }

            [data-testid="stMarkdownContainer"]{
                color: 	#FFFFFF !important;
            }

            h1{
                color: 	#FFFFFF !important;
            }
            #project-phonepe-pulse-visualization {
                color: white;
            }

            #custom-container {
                background-color: #0B030F !important;
                border-radius: 10px; /* Rounded corners */
                margin: 20px; /* Margin */
                padding: 20px;
            }

            #custom-container1 {
                background-color: #270C34 !important;
                border-radius: 10px; /* Rounded corners */
                margin: 20px; /* Margin */
                padding: 20px;
                text-align:left;
            }

            #custom-container2 {
                background-color: #270C34 !important;
                font-size: 25px;
                font-weight:bold;
            }
            .stPlotlyChart {
                background-color: #221542 !important;
            }

            [data-testid="baseButton-headerNoPadding"]{
                 background-color: white !important;   
            }
            
            
        </style>
    """
    st.markdown(styles, unsafe_allow_html=True)
#------------------------------------------------------------------------------------------------#   


# Setting up page configuration
def set_page_config():
    icon = Image.open("images/phonepe_logo_img.png")
    st.set_page_config(page_title= "Phonepe Pulse",
                    page_icon= icon,
                    layout= "wide",
                    initial_sidebar_state= "expanded",
                    menu_items={'About': """# This dashboard app is created by Aastha Mukherjee!"""})

#-------------------------------------------------------------------------------------------------#




# Custom function to create a top header with a logo
def top_header():
    # Add the logo to the top header
    col1,col2,col3,col4 = st.columns(4)
    with col1:
      st.image("images/download.svg", width=100)
    with col2:
      st.text("₹₹₹₹₹ Beat the progress")
#-------------------------------------------------------------------------------------------------#    

# Custom function for menu -  HOME PAGE
def menu_home(selected):
    conn = psycopg2.connect(database="phonepe_db",host="localhost",user="postgres",password="root",port="5432")
    cursor = conn.cursor()
    if selected == "Home":
        col1,col2 = st.columns([3,2],gap="medium")
        with col1:
            st.markdown(f"""
                <div id="custom-container2">A User-Friendly Tool Using Streamlit and Plotly</div>"""
            ,unsafe_allow_html=True)
        with col2:
            st.image("images/home.jpeg")

        cursor.execute("""
                   SELECT transaction_type, sum(transaction_count)as Total_Count,sum(transaction_amount)
                   as Total_amount FROM agg_trans 
                   group by transaction_type order by transaction_type""")
                
        df = pd.DataFrame(cursor.fetchall(), columns=['transaction_type', 'Total_Count','Total_amount'])
        df['Total_amount'].fillna(0, inplace=True)
        df['Total_Count'].fillna(0, inplace=True)

        col1,col2 = st.columns(2)
        with col1:
            total_count=int(df['Total_Count'].sum())
            formatted_total_count = '{:,}'.format(total_count)
            total_sum=int(df['Total_amount'].sum())/10000000
            formatted_total_sum = '₹ {:,} Cr'.format(total_sum)
            avg_sum=int(df['Total_amount'].mean())
            formatted_avg_sum = '₹ {:,}'.format(avg_sum)

            with st.container():
                st.markdown(
                    f"""
                    <div id="custom-container">
                        <p style="color: #04D9F6; font-family: 'Arial', sans-serif; font-size: 20px; font-weight: bold;">Transactions</p>
                        <p style="color: white; font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold;">All PhonePe transactions (UPI + Cards + Wallets)</p>
                        <p style="color: #04D9F6; font-family: 'Times New Roman', sans-serif; font-size: 30px; font-weight: bold;">{formatted_total_count}</p>
                        <div style="background-color: #04D9F6; height: 2px;"></div><br>
                        <p style="color: white; font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold;">Total Payment Value</p>
                        <p style="color: #04D9F6; font-family: 'Times New Roman', sans-serif; font-size: 20px; font-weight: bold;">{formatted_total_sum}</p>
                        <p style="color: white; font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold;">Avg. Transaction Value</p>
                        <p style="color: #04D9F6; font-family: 'Times New Roman', sans-serif; font-size: 20px; font-weight: bold;">{formatted_avg_sum}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
       
        with col2:
            mp=2
            print(df[df['transaction_type']=='Financial Services']['Total_Count'])
            fs_count='{:,}'.format(int(df[df['transaction_type']=='Financial Services']['Total_Count'].iloc[0]))
            mp_count='{:,}'.format(int(df[df['transaction_type']=='Merchant payments']['Total_Count'].iloc[0]))
            p2p_count='{:,}'.format(int(df[df['transaction_type']=='Peer-to-peer payments']['Total_Count'].iloc[0]))
            rb_count='{:,}'.format(int(df[df['transaction_type']=='Recharge & bill payments']['Total_Count'].iloc[0]))
            others_count='{:,}'.format(int(df[df['transaction_type']=='Others']['Total_Count'].iloc[0]))
            with st.container():
                st.markdown(f'''<div id="custom-container">
                            <p style="color: #04D9F6; font-family: 'Arial', sans-serif; font-size: 20px; font-weight: bold;">Categories</p>
                            <div style="background-color: #04D9F6; height: 2px;"></div><br>
                            <p style="color: white; font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold;">Merchant Payments&emsp;&emsp;&emsp;&emsp;&emsp;<span style="color: #04D9F6;font-size: 15px;">{mp_count}</span></p>
                            <p style="color: white; font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold;">Peer-to-Peer Payments&emsp;&emsp;&emsp;&emsp;<span style="color: #04D9F6;font-size: 15px;">{p2p_count}</span></p>
                            <p style="color: white; font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold;">Recharge and bill payments&emsp;&emsp;<span style="color: #04D9F6;font-size: 15px;">{rb_count}</span></p>
                            <p style="color: white; font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold;">Financial Services&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<span style="color: #04D9F6;font-size: 15px;">{fs_count}</span></p>
                            <p style="color: white; font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold;">Others&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<span style="color: #04D9F6;font-size: 15px;">{others_count}</span></p>
                            <div style="background-color: #04D9F6; height: 2px;"></div>
                            </div>''', unsafe_allow_html=True)
    conn.commit()
    conn.close()


# Custom function to set the pie-charts
def set_pie_charts_transactions(Year,Quarter):
    conn = psycopg2.connect(database="phonepe_db",host="localhost",user="postgres",password="root",port="5432")
    cursor = conn.cursor()
    col1,col2 = st.columns([1,1],gap="small")

    # pie-chart depicting : Statewise transaction and amount ( agg_trans table )     
    with col1:
        st.markdown(f"""<div style="color: white; font-family: 'Arial', sans-serif; font-size: 25px; font-weight: bold;">State</div>""", unsafe_allow_html=True)
        cursor.execute("""
                    select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from agg_trans 
                    where year = %s and quarter = %s 
                    group by state order by Total desc limit 10""",(Year,Quarter))
                    
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
        fig = px.pie(df, values='Total_Amount',
                                    names='State',
                                    title='Top 10 States',
                                    color_discrete_sequence=px.colors.sequential.Cividis, #'Cividis','Agsunset'
                                    hover_data=['Transactions_Count'],
                                    labels={'Transactions_Count':'Transactions_Count'})

        fig.update_traces(textposition='inside', textinfo='percent+label',textfont=dict(size=30))
        st.plotly_chart(fig,use_container_width=True)

    # pie-chart depicting : Pincodewise transaction and amount  for a state ( top_trans table )
    with col2:
        st.markdown(f"""<div style="color: white; font-family: 'Arial', sans-serif; font-size: 25px; font-weight: bold;">Pincode</div>""", unsafe_allow_html=True)

        st.markdown(f"""<div style="color: white; font-family: 'Arial', sans-serif; font-size: 20px; font-weight: bold;">Select state</div>""", unsafe_allow_html=True)
        cursor.execute("select distinct state from map_trans")
        states_df = pd.DataFrame(cursor.fetchall(), columns=['state'])
        states_tuple=tuple(states_df['state'].to_list())
        state = st.selectbox("",states_tuple,index=29,key="1")

        cursor.execute("""
                        select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_trans 
                        where year = %s and quarter = %s and state= %s
                        group by pincode order by Total desc limit 10""",(Year,Quarter,state))

        # cursor.execute("""
        #     SELECT t.pincode, sum(t.Transaction_count) as Total_Transactions_Count,
        #     sum(t.Transaction_amount) as Total FROM top_trans t inner join map_trans m on 
        #     t.state = m.state where t.year = %s and t.quarter = %s and t.state=%s 
        #     and m.district=%s group by t.state,m.district,t.pincode limit 10""",(Year,Quarter,state,district))
                  
        df = pd.DataFrame(cursor.fetchall(), columns=['Pincode','Transactions_Count','Total_Amount'])
        fig = px.pie(df, values='Total_Amount',
                                    names='Pincode',
                                    title='Top 10 Pincodes',
                                    color_discrete_sequence=px.colors.sequential.Agsunset,
                                    hover_data=['Transactions_Count'],
                                    labels={'Transactions_Count':'Transactions_Count'})

        fig.update_traces(textposition='inside', textinfo='percent+label',textfont=dict(size=30))
        st.plotly_chart(fig,use_container_width=True)

    col1,col2 = st.columns([1,1],gap="small")
    # pie-chart depicting : Districtwise transaction and amount for a particular state ( map_trans table )
    with col1:
        st.markdown(f"""<div style="color: white; font-family: 'Arial', sans-serif; font-size: 25px; font-weight: bold;">Top 10 Districts for a Particular State</div>""", unsafe_allow_html=True)
        state = st.selectbox("",
                                    ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                                    'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                                    'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                                    'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                                    'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                                    'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=35,key="3")
            
        cursor.execute("""
                            select district , sum(Count) as Total_Count, sum(Amount) as Total from map_trans 
                            where state = %s and year = %s and quarter = %s 
                            group by district order by Total desc limit 10""",(state,Year,Quarter))
                        
        df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

        fig = px.pie(df, values='Total_Amount',
                                        names='District',
                                        title='Top 10 Districts',
                                        color_discrete_sequence=px.colors.sequential.RdBu,
                                        hover_data=['Transactions_Count'],
                                        labels={'Transactions_Count':'Transactions_Count'})

        fig.update_traces(textposition='inside', textinfo='percent+label',textfont=dict(size=30))
        st.plotly_chart(fig,use_container_width=True)

    conn.commit()
    conn.close()



# Custom function to set the pie-charts
def set_bar_charts_transactions(Year,Quarter):
    conn = psycopg2.connect(database="phonepe_db",host="localhost",user="postgres",password="root",port="5432")
    cursor = conn.cursor()
    
    # BAR CHART - TOP PAYMENT TYPE
    st.markdown(f"""<div style="color: #white; font-family: 'Arial', sans-serif; font-size: 25px; font-weight: bold;">Top Payment Type</div>""", unsafe_allow_html=True)
    cursor.execute("""
                    select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from agg_trans 
                    where year= %s and quarter = %s 
                    group by transaction_type order by Transaction_type""",(Year,Quarter))
    df = pd.DataFrame(cursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])
    fig = px.bar(df,
                    title='Transaction Types vs Total_Transactions',
                    x="Transaction_type",
                    y="Total_Transactions",
                    orientation='v',
                    color='Total_amount',
                    color_continuous_scale=px.colors.sequential.Inferno)
    
    st.plotly_chart(fig,use_container_width=False)

    # BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
    st.markdown("# ")
    st.markdown("# ")
    st.markdown("# ")
    st.markdown(f"""<div style="color: #white; font-family: 'Arial', sans-serif; font-size: 25px; font-weight: bold;">Select any State to explore more</div>""", unsafe_allow_html=True)
    selected_state = st.selectbox("",
                                ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                                'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                                'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                                'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                                'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                                'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=35)
         
    cursor.execute("""
                select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans 
                where year = %s and quarter = %s and State = %s 
                group by State, District,year,quarter order by state,district""",(Year,Quarter,selected_state))
        
    df1 = pd.DataFrame(cursor.fetchall(), columns=['State','District','Year','Quarter',
                                                            'Total_Transactions','Total_amount'])
    fig = px.bar(df1,
                        title=selected_state,
                        x="District",
                        y="Total_Transactions",
                        orientation='v',
                        color='Total_amount',
                        color_continuous_scale=px.colors.sequential.Viridis)
    st.plotly_chart(fig,use_container_width=True)
    
    conn.commit()
    conn.close()


# Custom function to set the pie-charts
def set_charts_users(Year,Quarter):
    conn = psycopg2.connect(database="phonepe_db",host="localhost",user="postgres",password="root",port="5432")
    cursor = conn.cursor()
    col1,col2 = st.columns([2,2],gap="small")
    
    # horizontal bar-chart : top 10 brands used by users ( agg_user )
    with col1:
            if Year==2023:
                print("hi")
                st.write("Sorry !! No Brand data for Year 2023 !!")
            else:
                st.markdown(f"""<div style="color: #white; font-family: 'Arial', sans-serif; font-size: 25px; font-weight: bold;">Brands</div>""", unsafe_allow_html=True)
                cursor.execute("""
                                select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user 
                                where year = %s and quarter = %s 
                                group by brands order by Total_Count desc limit 10""",(Year,Quarter))           
                df = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                                title='Top 10 Brands',
                                x="Total_Users",
                                y="Brand",
                                orientation='h',
                                color='Avg_Percentage',
                                color_continuous_scale=px.colors.sequential.Magma)
                
                st.plotly_chart(fig,use_container_width=True) 

    # horizontal bar-chart : top 10 districts ( map_user )
    with col2:
        st.markdown(f"""<div style="color: #white; font-family: 'Arial', sans-serif; font-size: 25px; font-weight: bold;">District</div>""", unsafe_allow_html=True)
        cursor.execute("""
                    select district, sum(Registered_User) as Total_Users, sum(app_opens) as Total_Appopens from map_user 
                    where year = %s and quarter = %s 
                    group by district order by Total_Users desc limit 10""",(Year,Quarter))
                
        df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(float)
        fig = px.bar(df,
                            title='Top 10 Districts',
                            x="Total_Users",
                            y="District",
                            orientation='h',
                            color='Total_Users',
                            color_continuous_scale=px.colors.sequential.Inferno)
        st.plotly_chart(fig,use_container_width=True)

    col3,col4 = st.columns([2,2],gap="small")
    # pie-chart : registered users of top 10 pincodes ( top_user )          
    with col3:
        st.markdown(f"""<div style="color: #white; font-family: 'Arial', sans-serif; font-size: 25px; font-weight: bold;">Pincode</div>""", unsafe_allow_html=True)
        cursor.execute("""
                    select Pincode, sum(Registered_Users) as Total_Users from top_user 
                    where year = %s and quarter = %s 
                    group by Pincode order by Total_Users desc limit 10""",(Year,Quarter))
                
        df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Total_Users'])
        fig = px.pie(df,
                            values='Total_Users',
                            names='Pincode',
                            title='Top 10 Pincodes',
                            color_discrete_sequence=px.colors.sequential.Plasma,
                            hover_data=['Total_Users'])
        fig.update_traces(textposition='inside', textinfo='percent+label',textfont=dict(size=30))
        st.plotly_chart(fig,use_container_width=True)
                
    # pie-chart : top 10 states with app_opens ( map_user )
    with col4:
        st.markdown(f"""<div style="color: #white; font-family: 'Arial', sans-serif; font-size: 25px; font-weight: bold;">State</div>""", unsafe_allow_html=True)
        cursor.execute("""
                    select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user 
                    where year = %s and quarter = %s 
                    group by state order by Total_Users desc limit 10""",(Year,Quarter))
                
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
        fig = px.pie(df, values='Total_Users',
                                names='State',
                                title='Top 10 States',
                                color_discrete_sequence=px.colors.sequential.Viridis,
                                hover_data=['Total_Appopens'],
                                labels={'Total_Appopens':'Total_Appopens'})

        fig.update_traces(textposition='inside', textinfo='percent+label',textfont=dict(size=30))
        st.plotly_chart(fig,use_container_width=True)

    # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
    st.markdown(f"""<div style="color: #white; font-family: 'Arial', sans-serif; font-size: 25px; font-weight: bold;">Select any State to explore more</div>""", unsafe_allow_html=True)
    selected_state = st.selectbox("",
                                ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                                'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                                'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                                'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                                'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                                'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=35,key="4")
        
    cursor.execute("""
                select State,year,quarter,District,sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user 
                where year = %s and quarter = %s and state = %s 
                group by State, District,year,quarter order by state,district""",(Year,Quarter,selected_state))
            
    df = pd.DataFrame(cursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
    df.Total_Users = df.Total_Users.astype(int)
            
    fig = px.bar(df,
                        title=selected_state,
                        x="District",
                        y="Total_Users",
                        orientation='v',
                        color='Total_Users',
                        color_continuous_scale=px.colors.sequential.YlOrRd)
    st.plotly_chart(fig,use_container_width=True)
    conn.commit()
    conn.close()




# Custom function for menu -  TOP CHARTS
def menu_top_charts(selected):
    if selected == "View Charts":
        st.markdown(f"""<div style="color: white; font-family: 'Arial', sans-serif; font-size: 40px; font-weight: bold;">Charts</div>""",unsafe_allow_html=True)
        Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
        colum1,colum2= st.columns([1,1.5],gap="large")
        with colum1:
            Year = st.slider("**Year**", min_value=2018, max_value=2023)
            Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
        with colum2:
            st.markdown(f'''<div id="custom-container">
                            <p style="color: #04D9F6; font-family: 'Arial', sans-serif; font-size: 20px; font-weight: bold;">From this menu we can get insights like :</p>
                            </div>''', unsafe_allow_html=True)
            st.info(
                    """
                    Overall ranking on a particular Year and Quarter.
                    - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                    - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                    - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                    """,icon="🔍"
                    )
        
        # Top Charts - TRANSACTIONS    
        if Type == "Transactions":
            if Year==2023 and Quarter==4:
                st.markdown(f"""<div id="custom-container1"> Sorry No Data to Display for 2023 Qtr 4!!!</div>""", unsafe_allow_html=True)
            else:
                set_pie_charts_transactions(Year,Quarter)
                set_bar_charts_transactions(Year,Quarter)

        # Top Charts - USERS          
        if Type == "Users":
            if Year==2023 and Quarter==4:
                st.markdown(f"""<div id="custom-container1"> Sorry No Data to Display for 2023 Qtr 4!!!</div>""", unsafe_allow_html=True)
            else:
                set_charts_users(Year,Quarter)
    


# Custom function for menu -  VIEW MAP
def menu_view_map(selected):
    conn = psycopg2.connect(database="phonepe_db",host="localhost",user="postgres",password="root",port="5432")
    cursor = conn.cursor()
    if selected == "View Map":
        st.markdown(f"""<div style="color: white; font-family: 'Arial', sans-serif; font-size: 40px; font-weight: bold;">Maps</div>""",unsafe_allow_html=True)
        Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2023)
        Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
        Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
        
        if Type == "Transactions":
            # No data present for Quarters 2,3 and 4 for Transactions
            if Year == 2023 and Quarter == 4:
                st.markdown(f"""<div id="custom-container1"> Sorry No Data to Display for 2023 Qtr 2,3,4 !!!</div>""", unsafe_allow_html=True)
            else:
                # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
                st.markdown(f"""<div style="color: white; font-family: 'Arial', sans-serif; font-size: 25px; font-weight: bold;">Overall State Data - Transactions Amount</div>""",unsafe_allow_html=True)
                cursor.execute("""
                        select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans 
                        where year = %s and quarter = %s 
                        group by state order by state""",(Year,Quarter))
                    
                df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
                df2 = pd.read_csv('Statenames.csv')
                df1.State = df2
                set_geo_map(df1,'Total_amount',df1.columns.tolist())


                # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
                st.markdown(f"""<div style="color: white; font-family: 'Arial', sans-serif; font-size: 25px; font-weight: bold;">Overall State Data - Transactions Count</div>""",unsafe_allow_html=True)
                cursor.execute("""
                        select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans 
                        where year = %s and quarter = %s
                        group by state order by state""",(Year,Quarter))
                
                df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
                df2 = pd.read_csv('Statenames.csv')
                df1.Total_Transactions = df1.Total_Transactions.astype(int)
                df1.State = df2
                set_geo_map(df1,'Total_Transactions',df1.columns.tolist())

            
            
        if Type == "Users":
            # No data present for Quarter 4 for Users
            if Year == 2023 and Quarter == 4:
                st.markdown(f"""<div id="custom-container1"> Sorry No Data to Display for 2023 Qtr 4!!!</div>""", unsafe_allow_html=True)
            else:
                # Overall State Data - TOTAL APPOPENS - INDIA MAP
                st.markdown(f"""<div style="color: white; font-family: 'Arial', sans-serif; font-size: 25px; font-weight: bold;">Overall State Data - User App opening frequency</div>""",unsafe_allow_html=True)
                cursor.execute("""
                    select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user 
                    where year = %s and quarter = %s
                    group by state order by state""",(Year,Quarter))
                
                df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
                df2 = pd.read_csv('Statenames.csv')
                df1.Total_Appopens = df1.Total_Appopens.astype(float)
                df1.State = df2
                set_geo_map(df1,'Total_Appopens',df1.columns.tolist())

    conn.commit()
    conn.close()


# Custom function for menu -  ABOUT PAGE
def menu_about(selected):
    if selected == "About":
        col1,col2 = st.columns([3,3],gap="medium")
        with col1:
            st.write(" ")
            st.write(" ")
            st.markdown(f"""<div style="color: white; font-family: 'Arial', sans-serif; font-size: 40px; font-weight: bold; text-align:left;">About PhonePe Pulse:</div>""",unsafe_allow_html=True)
            st.markdown(f"""<div id="custom-container1"> BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.</div>""",unsafe_allow_html=True)
            st.markdown(f"""<div style="color: white; font-family: 'Arial', sans-serif; font-size: 40px; font-weight: bold; text-align:left;">About PhonePe:</div>""",unsafe_allow_html=True)
            st.markdown(f"""<div id="custom-container1"> PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat</div>""",unsafe_allow_html=True)
            st.markdown(f"""<div style="color: white; font-family: 'Arial', sans-serif; font-size: 25px; font-weight: bold; text-align:left;">Image and content source ⬇️</div>""",unsafe_allow_html=True)
            # st.write("**:violet[Image and content source]** ")
            st.write("https://www.prnewswire.com/in/news-releases/phonepe-launches-the-pulse-of-digital-payments-india-s-first-interactive-geospatial-website-888262738.html")
            
        with col2:
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.image("images/PhonePe.jpg")

#-------------------------------------------------------------------------------------------#


# Custom function to create a side-bar
def set_sidebar():
    
    st.sidebar.markdown('<p style="color: white; font-size:18px">🦰 Hi Aastha !!!</p>',unsafe_allow_html=True)
    with st.sidebar:
        selected = option_menu("Menu", ["Home","View Map","View Charts","About"], 
                    icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                    menu_icon= "menu-button-wide",
                    default_index=0,
                    styles={"nav-link": {"font-size": "15px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                            "nav-link-selected": {"background-color": "#B1A3F7"}})
    
    # MENU 1 - HOME
    menu_home(selected)           

    # MENU 2 - TOP CHARTS
    menu_top_charts(selected)
            
    # MENU 3 - VIEW MAP
    menu_view_map(selected)

    # MENU 4 - ABOUT
    menu_about(selected)


#-----------------------------------------------------------#
    

def set_geo_map(df1,color,ls):
        fig = px.choropleth(
            df1,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            color=color,
            color_continuous_scale='YlGnBu',   # 'YlOrRd', 'Plasma','Inferno','Magma','RdBu','YlGnBu'
            hover_data=ls
        )
        
        fig.update_geos(fitbounds="locations", visible=False)
        
        
        fig.update_layout(
            geo=dict(
                 bgcolor='#270C34'
            ),
            paper_bgcolor='#270C34',
            coloraxis_colorbar=dict(
                title={'text': color, 'font': {'color': 'white', 'size': 20}},
                tickfont=dict(color='white', size=20)
            ),
            hoverlabel=dict(
                bgcolor='#FFDC2C',  # background color
                font=dict(color='black', size=20),  # font color and size
                bordercolor='rgba(0, 0, 0, 0.2)',  # border color
            ),
            height=800,
            width=700
        )
        
        st.plotly_chart(fig,use_container_width=True)
    
#-----------------------------------------------------------#


# Custom Function to set the different components in the page
def set_components():
    set_css()
    top_header()
    set_sidebar()
#-----------------------------------------------------------#


#============================ MAIN FUNCTION ======================================#
if __name__ == "__main__":
    set_page_config()

    header = st.container()
    with header:
        set_components()
        
    
####################################################################################