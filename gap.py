import pandas as pd
import numpy as np
df=pd.read_excel('D:\python\pyanalysis\exercise\练习1数据.xlsx',skiprows=1)
#print(df.课程1学分)
df['GAP']=round((df.课程1学分*df.课程1成绩+df.课程2学分*df.课程2成绩+df.课程3学分*df.课程3成绩)/(df.课程1学分+df.课程2学分+df.课程3学分),2)
print(df)