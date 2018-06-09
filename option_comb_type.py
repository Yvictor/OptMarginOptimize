
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


# In[65]:


df_a.loc[2:2, 'SELECTED'] = 1


# In[66]:


df_a['COMBTYPE'] = 0


# In[67]:


df_a


# In[78]:


df_a[df_a['SELECTED'] == 1]


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

