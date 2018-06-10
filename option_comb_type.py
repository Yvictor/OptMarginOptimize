
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[61]:


df_a = pd.read_msgpack('data/df_a.msgpack')
df_b = pd.read_msgpack('data/df_b.msgpack')
df_c = pd.read_msgpack('data/df_c.msgpack')


# In[3]:


df_a


# In[62]:


df_a = pd.concat([df_a, df_b[df_b.columns[:8]].rename(columns=lambda x: x[:-1]),
                  df_b[df_b.columns[8:16]].rename(columns=lambda x: x[:-1])], 
                  sort=False).reset_index(drop=True)


# In[63]:


df_a['SELECTED'] = '0'


# In[6]:


df_a.loc[0, 'STOCK']


# In[13]:


df_a[df_a['POC'] == 'P']


# In[16]:


df_a[df_a['POC'] == 'P'].iloc[2:]


# In[64]:


df_a


# In[19]:


type(df_a[df_a['POC'] == 'P'].loc[4])


# In[20]:


type(df_a[df_a['POC'] == 'P'].iloc[2:])


# In[33]:


df_a.loc[2]


# In[89]:


df_a['STOCK'].unique()


# In[65]:


df_a.loc[2:2, 'SELECTED'] = 1


# In[66]:


df_a['COMBTYPE'] = 0


# In[67]:


df_a


# In[96]:


comb1 = df_a[df_a['SELECTED'] == 1].iloc[0]


# In[97]:


comb1


# In[86]:


comb1['SMONTH']


# In[105]:


unselected = df_a['SELECTED'] != 1
df_remain = df_a[unselected]


# In[84]:


df_remain


# # Same EXdate Spread Comb 

# In[108]:


df_a.loc[(unselected) &         (df_a['STOCK'] == comb1.STOCK) &         (df_a['SMONTH'] == comb1.SMONTH) &         (df_a['POC'] == comb1.POC) &         (df_a['BS'] != comb1.BS), 
        'COMBTYPE'] = 1


# # Strangle & Straddle

# In[151]:


df_a.loc[(unselected) &         (df_a['STOCK'] == comb1.STOCK) &         (df_a['SMONTH'] == comb1.SMONTH) &         (df_a['POC'] != comb1.POC) &         (df_a['BS'].map(lambda x: comb1.BS == 'S' and x == comb1.BS )),
        'COMBTYPE'] = 2


# # Calendar Spread

# In[146]:


df_a.loc[(unselected) &         (df_a['STOCK'] == comb1.STOCK) &         (df_a['SMONTH'].map(lambda x: x > comb1.SMONTH if comb1.BS == 'S' else x < comb1.SMONTH)) &         (df_a['POC'] == comb1.POC) &         (df_a['BS'] != comb1.BS), 
        'COMBTYPE'] = 3


# ```
# if comb1.BS == 'S':
#     df_a.loc[(unselected) & \
#             (df_a['STOCK'] == comb1.STOCK) & \
#             (df_a['SMONTH'] > comb1.SMONTH) & \
#             (df_a['POC'] == comb1.POC) & \
#             (df_a['BS'] != comb1.BS), 
#             'COMBTYPE'] = 3
# else:
#     df_a.loc[(unselected) & \
#             (df_a['STOCK'] == comb1.STOCK) & \
#             (df_a['SMONTH'] < comb1.SMONTH) & \
#             (df_a['POC'] == comb1.POC) & \
#             (df_a['BS'] != comb1.BS), 
#             'COMBTYPE'] = 3
# ```

# In[152]:


df_a


# # Same EXdate Spread Comb Calculate

# In[187]:


contract_multiplier = {'TXO       ': 50}


# In[188]:


contract_multiplier


# In[155]:


df_a.loc[df_a['COMBTYPE']==1, 'SELECTED'] = 1


# In[156]:


df_a


# In[158]:


combs = df_a[df_a['SELECTED']==1]


# In[175]:


combs['POC'].map(lambda x: 1 if x=='C' else -1).iloc[0]


# In[194]:


PC = {'C': 1, 'P': -1}
((combs.loc[combs['BS']=='S', 'SPRICE'].reset_index(drop=True) - combs.loc[combs['BS']=='B', 'SPRICE'].reset_index(drop=True)) * combs['POC'].map(lambda x: PC[x]).iloc[0]).clip(lower=0)*contract_multiplier.get(combs.STOCK.iloc[0])


# In[199]:


get_ipython().run_cell_magic(u'timeit', u'', u"PC = {'C': 1, 'P': -1}\n((combs.loc[combs['BS']=='S', 'SPRICE'].reset_index(drop=True) - \\\ncombs.loc[combs['BS']=='B', 'SPRICE'].reset_index(drop=True)) * \\\ncombs['POC'].map(lambda x: PC[x]).iloc[0]).clip(lower=0)*contract_multiplier.get(combs.STOCK.iloc[0])")


# In[203]:


get_ipython().run_cell_magic(u'timeit', u'', u"same_exdate_spread(combs.loc[combs['BS']=='S', 'SPRICE'].iloc[0], combs.loc[combs['BS']=='B', 'SPRICE'].iloc[0], \n                   combs['POC'].map(lambda x: PC[x]).iloc[0], contract_multiplier.get(combs.STOCK.iloc[0], 50))")


# In[216]:


get_ipython().run_cell_magic(u'timeit', u'', u"same_exdate_spread(combs.loc[combs['BS']=='S', 'SPRICE'].iloc[0], combs.loc[combs['BS']=='B', 'SPRICE'].iloc[0], \n                   PC.get(combs['POC'].iloc[0], 1), contract_multiplier.get(combs.STOCK.iloc[0], 50))")


# In[215]:


get_ipython().run_cell_magic(u'timeit', u'', u"PC.get(combs['POC'].iloc[0], 1)")


# In[209]:


get_ipython().run_cell_magic(u'timeit', u'', u"combs['POC'].map(lambda x: PC[x])")


# In[207]:


get_ipython().run_cell_magic(u'timeit', u'', u'same_exdate_spread(10000, 12000, 1, 50)')


# In[198]:


def clip(x, lower=0):
    if x > lower:
        return x
    else:
        return 0


# In[197]:


def same_exdate_spread(sell_strike_price, buy_strike_price, cp, contract_multipier):
    return clip((sell_strike_price - buy_strike_price)*cp)*contract_multipier


# In[166]:


get_ipython().run_cell_magic(u'timeit', u'', u"combs.loc[combs['BS']=='S', 'SPRICE'] ")


# In[169]:


get_ipython().run_cell_magic(u'timeit', u'', u"combs.loc[combs['BS']=='S', 'SPRICE'].reset_index(drop=True)")


# In[220]:


df_a.loc[df_a['COMBTYPE']==1, 'SELECTED'] = 0


# # Calendar Spread

# In[218]:


df_a.loc[df_a['COMBTYPE']==3, 'SELECTED'] = 1


# In[224]:


df_a


# In[225]:


combs = df_a[df_a['SELECTED']==1]
combs


# In[222]:


def calendar_spread(strike_product_margin, sell_price, buy_price, contract_multipier):
    return max(strike_product_margin*0.1, 2 * abs(sell_price - buy_price) * contract_multipier)


# In[223]:


STK_PROD_MARGIN = {'TXO       ': 83000}


# In[237]:


calendar_spread(STK_PROD_MARGIN.get(combs.STOCK.iloc[0], 83000), combs[combs['BS'] == 'S']['SPRICE'].iloc[0], 
                combs[combs['BS'] == 'B']['SPRICE'].iloc[0], contract_multiplier.get(combs.STOCK.iloc[0], 50))


# In[238]:


get_ipython().run_cell_magic(u'timeit', u'', u"calendar_spread(STK_PROD_MARGIN.get(combs.STOCK.iloc[0], 83000), combs[combs['BS'] == 'S']['SPRICE'].iloc[0], \n                combs[combs['BS'] == 'B']['SPRICE'].iloc[0], contract_multiplier.get(combs.STOCK.iloc[0], 50))")


# In[240]:


df_a.loc[df_a['COMBTYPE']==3, 'SELECTED'] = 0


# # Strangle & Straddle Calculate

# In[245]:


df_a.loc[7, 'POC'] = 'P'


# In[254]:


df_a.loc[7, 'OTAMT'] = 25000.0


# In[331]:


df_a.loc[7, 'PRICE'] = 110.


# In[255]:


df_a.loc[(unselected) &         (df_a['STOCK'] == comb1.STOCK) &         (df_a['SMONTH'] == comb1.SMONTH) &         (df_a['POC'] != comb1.POC) &         (df_a['BS'].map(lambda x: comb1.BS == 'S' and x == comb1.BS )),
        'COMBTYPE'] = 2


# In[256]:


df_a.loc[df_a['COMBTYPE']==2, 'SELECTED'] = 1


# In[257]:


df_a


# In[332]:


combs = df_a[df_a['SELECTED']==1]


# In[333]:


combs


# In[334]:


combs[combs['POC']=='P']


# In[335]:


combs[combs['POC']=='C']


# In[336]:


get_ipython().run_cell_magic(u'timeit', u'', u"combs.sort_values('OTAMT', ascending=False)[['OTAMT', 'PRICE']].values * np.eye(2)")


# In[337]:


get_ipython().run_cell_magic(u'timeit', u'', u"combs[['OTAMT', 'PRICE']].values")


# In[344]:


a = combs[['OTAMT', 'PRICE']].values
(a[a[:, 0].argsort()[::-1]] * np.eye(2)).sum()


# In[345]:


def stra_comb(arr):
    return (arr[arr[:, 0].argsort()[::-1]] * np.eye(2)).sum()


# In[346]:


get_ipython().run_cell_magic(u'timeit', u'', u"stra_comb(combs[['OTAMT', 'PRICE']].values)")


# In[343]:


get_ipython().run_cell_magic(u'timeit', u'', u'(a[a[:, 0].argsort()[::-1]] * np.eye(2)).sum()')


# In[340]:


a[a[:, 0].argsort()]


# In[316]:


get_ipython().run_cell_magic(u'timeit', u'', u"combs.sort_values('OTAMT', ascending=False)")


# In[318]:


get_ipython().run_cell_magic(u'timeit', u'', u"combs[['OTAMT', 'PRICE']]")


# In[312]:


get_ipython().run_cell_magic(u'timeit', u'', u"(combs.sort_values('POC')[['OTAMT', 'PRICE']].values * np.eye(2)).sum()")


# In[305]:


a = {'C': {'OTAMT': 25000,
       'PRICE': 159.0},
'P': {'OTAMT': 34350,
       'PRICE': 159.0}}


# In[306]:


np.array([a['C']['OTAMT'], a['P']['OTAMT']])


# In[307]:


conv_ind_pc = {0: 'C', 1: 'P'}
conv_ind_pc


# In[308]:


np.argmin(np.array([a['C']['OTAMT'], a['P']['OTAMT']]))


# In[311]:


get_ipython().run_cell_magic(u'timeit', u'', u"max(a['C']['OTAMT'], a['P']['OTAMT']) + a[conv_ind_pc[np.argmin(np.array([a['C']['OTAMT'], a['P']['OTAMT']]))]]['PRICE']*50")


# In[310]:


a[conv_ind_pc[np.argmin(np.array([a['C']['OTAMT'], a['P']['OTAMT']]))]]['PRICE']*50


# In[274]:


max(a['C']['OTAMT'], a['P']['OTAMT'])


# In[275]:


min(a['C']['OTAMT'], a['P']['OTAMT'])


# In[127]:


df_a.loc[(unselected) &         (df_a['STOCK'] == comb1.STOCK) &         (df_a['SMONTH'].map(lambda x: if len(x)==6) > comb1.SMONTH) &         (df_a['POC'] == comb1.POC) &         (df_a['BS'] != comb1.BS), 
        ]#'COMBTYPE']


# In[141]:


df_a.loc[(unselected) &         (df_a['STOCK'] == comb1.STOCK) &         (df_a['SMONTH'] > comb1.SMONTH) &         (df_a['POC'] == comb1.POC) &         (df_a['BS'] != comb1.BS), 
        'COMBTYPE'] = 3


# In[140]:


comb1


# In[138]:


df_a['SMONTH'].map(lambda x: x+'W3' if len(x)==6 else x)


# In[128]:


comb1


# In[109]:


df_a


# In[71]:


def clip(x):
    if x > 0:
        return x
    else:
        return 0


# In[79]:


POC = 1
clip((11100 - 11200)*POC)*50


# In[45]:


df_b[df_b.columns[:8]].rename(columns=lambda x: x[:-1])


# In[50]:


df_b.columns[8:16]


# In[41]:


df_b


# In[ ]:


df_a

