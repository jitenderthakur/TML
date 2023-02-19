import pandas as pd
import fpdf

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from sqlalchemy import create_engine
from datetime import date
from datetime import datetime
from datetime import timedelta
import time
import logging as lg

import ConnectDb
from ConnectDb import postgreSql

from ConnectDb import sql
import configparser

# db
config_Url = configparser.ConfigParser()
config_Url.read('database.ini')
sql_username = config_Url["SQL"]["sql_username"]
sql_password = config_Url["SQL"]["sql_password"]
sql_ip = config_Url["SQL"]["sql_ip"]
sql_port = config_Url["SQL"]["sql_port"]
sql_database = config_Url["SQL"]["sql_database"]


#logging
logger = lg.basicConfig(filename = "C:/Users/HP/Desktop/Mukesh/tml_pipeline/log_files/"+"report_creation"+str(datetime.now().date())+".log", 
                        level = lg.INFO, 
                        format = '%(asctime)s %(message)s')
algo8_python_logger = lg.getLogger()

# connect to database
db = sql()
db_conn = db.connect_with_sql(sql_username,sql_password,sql_ip,sql_port, sql_database)



    
        
def dataframe_to_pdf(df, path):
	"""this fxn will convert dataframe to pdf"""
	# https://stackoverflow.com/questions/32137396/how-do-i-plot-only-a-table-in-matplotlib
	algo8_python_logger.info({"message": "Convert DataFrame to PDF"})
	
	fig, ax = plt.subplots(figsize=(12, 4))
	ax.axis('tight')
	ax.axis('off')
	the_table = ax.table(cellText=df.values,
						 colLabels=df.columns, loc='center')

	# https://stackoverflow.com/questions/4042192/reduce-left-and-right-margins-in-matplotlib-plot
	today = str(date.today())
	now = datetime.now()
	curr_time = str(now.strftime("%H:%M:%S"))
	current_time = str(now.strftime("_%H"))
	report_name='tml_'+today+'.pdf'    
	pp = PdfPages(path+'tml_'+today+curr_time+".pdf")
# 	engine.execute('''insert into hzl.report (date, time, reportName, sent) values ('{}','{}','{}',0)'''.format(today,curr_time,report_name))
# 	print('data inserted')
	pp.savefig(fig, bbox_inches='tight')
	#sendReport("subject","HZL_PDF_REPORT_DAILY",pp,"shivam.kumar@algo8.ai","pramod.jangid@algo8.ai")
	pp.close()        

def one_hr_df_pdf(time):
    """this fxn will create table pdf report
        with hourly time period of whole dayy"""

    #fetching previous 1day data
    algo8_python_logger.info({"message": "One day Data Fetch from DataBase"})

    query = '''select timeStamp,ImageName,MoldCount,UnderSize,OverSize,NormalSize
         from TML_data where timestamp >= '{}' '''.format(time)

    _,data=db.fetch_details(query,db_conn[1])
    # creating df of the above output
    df = pd.DataFrame(data,columns=['timeStamp', 'ImageName', 'MoldCount', 'UnderSize', 'OverSize','NormalSize'])

    if not df.empty:
        #convert it to datetime
        df['TimeStamp']= pd.to_datetime(df['timeStamp'])

        # add total defected column
        df['total_defected_ingots']=df[['UnderSize','OverSize']].apply(lambda x: 0 if  x[0]==0 | x[1]==0 else 1,axis=1)

        #add column total ingot
        df['total_MoldCount']=1
        # resampling df
        df= df.set_index('TimeStamp').resample('60min').sum()

        #converting inddex to column
        df=df.reset_index().rename({'index':'index1'},axis='columns')
        #convert df to pdf
        # final pdf path where pdf will be stored
        final_pdf_path = 'C:/Users/HP/Desktop/Mukesh/tml_pipeline/'
        dataframe_to_pdf(df,final_pdf_path)	
        algo8_python_logger.info({"message": "Sucessfully Saved one day pdf "})    
    
        
#one_hr_df_pdf(time)
