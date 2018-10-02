
# coding: utf-8

# <h1>Chipotle Data Analysis</h1>
# Importing Libraries

# In[16]:


import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sb
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import squarify
import warnings


# In[29]:


warnings.filterwarnings("ignore")


# <b>Defining Functions</b>

# In[2]:


def marking_units(quantity) :
    if quantity <= 0 :
        return 0
    if quantity >= 1 :
        return 1


# Reading Data from a CSV file..

# In[3]:


data = pd.read_csv("C:/Users/rrs140/Documents/Chipotle/chipotle/chipotle.tsv" , sep ="\t")


# In[4]:


print("\n\t-----\tEntire Dataset.\t-----\t\n")
print(data)


# Removing "$" sign from the price coloumn

# In[5]:


data['item_price'] = data['item_price'].str.replace('$','')


# Converting price to a Float

# In[6]:


data['item_price'] =  data['item_price'].astype(float) 


# If you observe the data, a few items have missing item descriptions,
# Thus we will populate them with their respective item names..

# In[7]:


data['items'] = data['item_name']
data['items'] = data['items'].str.replace('and',',')
for i in range(len(data['order_id'])):
    if pd.isnull(data['choice_description'][i]):
        data['choice_description'][i] = str('['+data['items'][i]+']')


# In[8]:


print("\n\t-----\tDataset After Cleaning\t-----\t\n")
print(data)


# Finding popular items

# In[9]:


popular_items = data.groupby(data['item_name'])['item_name'].count()
print("\n\t-----\tDisplaying Quantities of Menu Items sold.\t-----\t\n")
print(popular_items.sort_values(ascending = False))


# The menu items in chipotle can be broadly divided in 6 categories : 
# We shall divide all the orders into these 6 categories.

# In[10]:


data['item_name'] = data['item_name'].astype(str)
df = pd.DataFrame(data)
bowls_count = burritos_count = chips_count = drinks_count = salad_count = tacos_count = other = 0


# <b>Categorizing the orders :</b>

# In[11]:


for i in range(len(data['order_id'])) :
    if df['item_name'][i].find("Bowl") > -1:
        bowls_count += 1
    elif df['item_name'][i].find("Burrito") > -1:
        burritos_count += 1
    elif df['item_name'][i].find("Chips") > -1:
        chips_count += 1
    elif df['item_name'][i].find("Drink") > -1 or  df['item_name'][i].find("Water") > -1 or df['item_name'][i].find("Izze") > -1 or        df['item_name'][i].find("Nectar") > -1  or df['item_name'][i].find("Soda") > -1:
        drinks_count += 1
        #print(df['item_name'][i],"\t",drinks_count)
    elif df['item_name'][i].find("Salad") > -1:
        salad_count += 1
    elif df['item_name'][i].find("Tacos") > -1:
        tacos_count += 1
    else:
        other +=1
        print(df['item_name'][i],"\t",other)


# In[12]:


Names = ['Bowls','Burritos','Tacos','Chips','Salads','Drinks']
Total = [bowls_count,burritos_count,tacos_count,chips_count,salad_count,drinks_count]
Table = pd.DataFrame({'Item Name': Names,'Total': Total,})
print("\n\t-----\tCategorizing the orders.\t-----\t\n")
print(Table.sort_values(by = 'Total', ascending = False))


# In[13]:


sb.set_style("white")
sb.set_context("notebook")
col = sb.color_palette("Blues_d")
explode = (0.05,0.05,0.05,0.05,0.05,0.05)

figure, axis_pie = plt.subplots()
axis_pie.pie(Table['Total'],explode =explode, labels=Table['Item Name'], autopct='%1.1f%%', colors = col)
axis_pie.axis('equal') 
plt.title("Chart for Menu Item Categories.")
plt.show()


# <h2> BOWLS </h2>
# Now we will look
# further into Bowls. We will find the most popular bowls.

# In[14]:


bowls = []

for i in range(len(df)) :
    if df['item_name'][i].find("Bowl") > -1:
        bowls.append(df['item_name'][i])

bowls_df = pd.DataFrame(bowls)
bowls_df.rename(columns={0:'Item'},inplace = True)


sb.set_style("white")
sb.set_context("talk")

bowls_df1 = bowls_df.groupby('Item')['Item'].count()

with sb.color_palette("Blues_d"):bowls_df1.sort_values(ascending = False).plot(kind = 'bar')
plt.title("The graph displays the popularity of various types of bowls in chipotle")
plt.show()


# <b>The above graph displays the popularity of various types of bowls in chipotle</b>

# <h2>Burritos</h2>
# Now we will look further into Burritos. We will find the most popular burritos.

# In[15]:


burritos = []

for i in range(len(df)) :
    if df['item_name'][i].find("Burrito") > -1:
        burritos.append(df['item_name'][i])

burritos_df = pd.DataFrame(burritos)
burritos_df.rename(columns={0:'Item'},inplace = True)


burritos_df1 = burritos_df.groupby('Item')['Item'].count()
with sb.color_palette("PuBuGn_d"):burritos_df1.sort_values(ascending = False).plot(kind = 'bar')
plt.title("The graph displays the popularity of various types of burritos in chipotle")
plt.show()


# <b>The above graph displays the popularity of various types of burritos in chipotle</b>

# <h2>Chips</h2>
# Now we will look further into Chips. We will find the most popular chips & their sides.

# In[17]:


chips = []

for i in range(len(df)) :
    if df['item_name'][i].find("Chips") > -1:
        chips.append(df['item_name'][i])

chips_df = pd.DataFrame(chips)
chips_df.rename(columns={0:'Item'},inplace = True)

chips_df1 = chips_df.groupby('Item')['Item'].count()
with sb.color_palette("PuBuGn_d"):chips_df1.sort_values(ascending = False).plot(kind = 'bar')
plt.title("The graph displays the popularity of various types of chips in chipotle")
plt.show()


# <b>The above graph displays the popularity of various types of chips in chipotle</b>

# <h2>Salads</h2>
# Now we will look further into Salads. We will find the most popular Salads

# In[18]:


salads = []

for i in range(len(df)) :
    if df['item_name'][i].find("Bowl") > -1:
           continue
    elif df['item_name'][i].find("Salad") > -1:
        salads.append(df['item_name'][i])

salad_df = pd.DataFrame(salads)
salad_df.rename(columns={0:'Item'},inplace = True)

salad_df1 = salad_df.groupby('Item')['Item'].count()
with sb.color_palette("PuBuGn_d"):salad_df1.sort_values(ascending = False).plot(kind = 'bar')
plt.title("The graph displays the popularity of various types of salads in chipotle")
plt.show()


# <b>The above graph displays the popularity of various types of salads in chipotle</b>

# <h2>Tacos</h2>
# Now we will look further into Tacos. We will find the most popular Tacos

# In[19]:


tacos = []

for i in range(len(df)) :
    if df['item_name'][i].find("Tacos") > -1:
        tacos.append(df['item_name'][i])

tacos_df = pd.DataFrame(tacos)
tacos_df.rename(columns={0:'Item'},inplace=True)

tacos_df1 = tacos_df.groupby('Item')['Item'].count()
with sb.color_palette("PuBuGn_d"):tacos_df1.sort_values(ascending = False).plot(kind = 'bar')
plt.title("The graph displays the popularity of various types of tacos in chipotle")
plt.show()


# <b>The above graph displays the popularity of various types of tacos in chipotle</b>

# <h2>Drinks</h2>
# Now we will look further into Drinks. We will find the most popular Drinks

# In[20]:


drinks = []
drink_types = []

for i in range(len(df)) :
    if df['item_name'][i].find("Drink") > -1 or  df['item_name'][i].find("Water") > -1 or df['item_name'][i].find("Izze") > -1 or        df['item_name'][i].find("Nectar") > -1  or df['item_name'][i].find("Soda") > -1:
        drinks.append(df['item_name'][i])
        if df['item_name'][i].find("Drink") > -1 :
            drink_types.append(df['choice_description'][i])

drinks_df = pd.DataFrame(drinks)
drinks_df.rename(columns={0:'Item'},inplace=True)
drinks_df1 = drinks_df.groupby('Item')['Item'].count()
with sb.color_palette("PuBuGn_d"):drinks_df1.sort_values(ascending = False).plot(kind = 'bar')  
plt.title("The graph displays the popularity of various types of Drinks in chipotle")
plt.show()


# <b>The above graph displays the popularity of various types of Drinks in chipotle</b>

# Canned Soft Drinks & Canned Sodas

# In[21]:


drinks_types = pd.DataFrame(drink_types)
drinks_types
drinks_types.rename(columns={0:'Item'},inplace=True)
drinks_types = drinks_types.groupby('Item')['Item'].count()
with sb.color_palette("PuBuGn_d"):drinks_types.sort_values(ascending = False).plot(kind = 'bar')
plt.title("The graph displays the popularity of various sub-types of drinks in chipotle")
plt.show()


# <b>The above graph displays the popularity of various sub-types of drinks
#  in chipotle</b>

# <h2>Market Basket Analysis using association rules</h2>
# Market Basket Analysis is popularly known for finding hidden patterns in big data sets. It is employed by retailers to find useful combinations from users buying habits. 
# We will be using this analysis to find multiple insights in the Chipotle Data.

# In[ ]:


print("\n\t-----\tMarket Basket Analysis using association rules\t-----\t\n")


# In[22]:


basket = df.groupby(['order_id','item_name'] )['quantity'].sum().unstack().reset_index().fillna(0).set_index('order_id')
print(basket.head())


# In[23]:


basket_sets = basket.applymap(marking_units)
frequent_itemsets = apriori(basket_sets, min_support = 0.05, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.20)
print("\n")
print("\n\t-----\tAssociation rules with values above Minimum Support(5%) and Minimum Confidence Threshold(20%).\t-----\t\n")
print(rules)


# Minimum support is being set at 5%. <br>
# This is because of the size of the data.

# <h4>Now will use association rules on ingridients, to determine their dependence on each other.</h4>

# In[24]:


in_df = data
in_df['choice_description'] = data['choice_description'].str.replace('[','')
in_df['choice_description'] = data['choice_description'].str.replace(']','')

in_df['choice_description'] = in_df['choice_description'].astype(str)

in_list = []
for i in range(len(in_df)):
    in_list.append(in_df['choice_description'][i].split(","))
    
in_df = pd.DataFrame(in_list)
aa = []

for i in range(len(data)):
    ss = data['item_name'][i].split()
    ax = ss[0]
    aa.append(ax)

in_df['item_name'] = aa
print("\n")
print("\n\t-----\tAssociation rules on ingridients, to determine their dependence on each other.\t-----\t\n")
print(in_df)    
    


# In[25]:


in_df.rename(columns={0:'',1:'',2:'',3:'',4:'',5:'',6:'',7:'',8:'',9:''},inplace = True)

dummy = in_df.stack().reset_index()

for i in range(len(dummy)):
    dummy.loc[i,0] = dummy.loc[i,0].strip()
    stringParts = dummy.loc[i,0].split("-")
    dummy.loc[i,0] = " ".join(stringParts)


# In[26]:


basket1 = dummy.groupby(['level_0',0] )[0].count().unstack().reset_index().fillna(0).set_index('level_0')
basket1.columns

frequent_itemsets1 = apriori(basket1, min_support = 0.06, use_colnames=True)
rules1 = association_rules(frequent_itemsets1, metric="conviction", min_threshold=4)
print("\n")
print(rules1)


# In[27]:


item = dummy.groupby(0)[0].count().sort_values(ascending = False).head()


# In[28]:


item_df = pd.DataFrame(item)
item_df.rename(columns={0:'Count'},inplace = True)
item_df = item_df.reset_index()
item_df.rename(columns={0:'Item'},inplace = True)
item_df

sb.set_context("poster")

squarify.plot(sizes=item_df['Count'],label = item_df['Item'], color = col, alpha = 0.9)
plt.axis('off')
plt.title("Chart of Most Frequently used ingredients")
plt.show()

