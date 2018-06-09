
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[11]:


get_ipython().system(u' ls -alh data')


# In[25]:


df_a = pd.read_pickle('data/df_a.pickle')


# In[26]:


df_a.DISPLAY = df_a.DISPLAY.map(lambda x: x.decode('cp950'))


# In[27]:


df_a.to_msgpack('data/df_a.msgpack')


# In[28]:


df_b = pd.read_pickle('data/df_b.pickle')


# In[29]:


df_b.to_msgpack('data/df_b.msgpack')


# In[30]:


df_c = pd.read_pickle('data/df_c.pickle')


# In[31]:


df_c.to_msgpack('data/df_c.msgpack')


# In[32]:


df_a = pd.read_msgpack('data/df_a.msgpack')
df_b = pd.read_msgpack('data/df_b.msgpack')
df_c = pd.read_msgpack('data/df_c.msgpack')


# In[36]:


df_a


# In[34]:


df_b


# In[35]:


df_c

