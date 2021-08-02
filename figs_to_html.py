import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import scipy.stats as sci 
from dateutil.relativedelta import relativedelta

df_price = pd.read_pickle('data/marketPrice.pkl')
df_vol = pd.read_pickle('data/marketVol.pkl')
#df_delta = pd.read_pickle('data/marketDelta.pkl')
df_overall_data = pd.read_pickle('data/marketData.pkl')


#preprocessing:
all_skins = list(df_price.columns)
skins_prefix_set = set([string.split('|')[0] for string in all_skins])
skins_prefix_set = set(string.rstrip().lstrip() for string in skins_prefix_set)
prefix_remaining = list(skins_prefix_set).copy()

def update_prefix_remaining(cataloged_type, prefix_remaining = prefix_remaining):
    for prefix in cataloged_type:
        try:
            prefix_remaining.remove(prefix)
        except:
            continue



#definindo um dicionário com os tipos de skins
types = {}

types['statTrak'] = [prefix for prefix in prefix_remaining if 'StatTrak™' in prefix]
update_prefix_remaining(types['statTrak'])

types['pistols'] = ['Glock-18','P2000', 'USP-S','P250', 'Dual Berettas', 'Tec-9' ,'Five-SeveN', 
                 'CZ75-Auto', 'Desert Eagle', 'R8 Revolver']
types['heavys'] =['Nova','XM1014','MAG-7','Sawed-Off','M249', 'Negev']
types['smgs'] = ['MAC-10', 'MP9', 'UMP-45', 'MP7', 'PP-Bizon', 'P90' , 'MP5-SD']
types['ars'] = ['Galil AR' , 'FAMAS', 'AK-47', 'M4A4', 'M4A1-S', 'SG 553', 'AUG']
types['snipers'] = ['SSG 08', 'AWP', 'G3SG1', 'SCAR-20']
types['weapons'] = types['pistols'] + types['heavys'] + types['smgs'] + types['ars'] + types['snipers']
update_prefix_remaining(types['weapons'])

types['pins'] = [prefix for prefix in prefix_remaining if 'Pin' in prefix]
update_prefix_remaining(types['pins'])

types['knifes'] = [prefix for prefix in prefix_remaining if 'Knife' in prefix]
types['knifes'] = types['knifes'] + ['★ Bayonet','★ M9 Bayonet','★ Karambit','★ Shadow Daggers']
update_prefix_remaining(types['knifes'])

types['gloves'] = [prefix for prefix in prefix_remaining if 'Gloves' in prefix]
types['gloves'] = types['gloves'] + ['★ Hand Wraps']
update_prefix_remaining(types['gloves'])

types['keys'] = [prefix for prefix in prefix_remaining if 'Case Key' in prefix]
types['keys'] = types['keys'] +['CS:GO Capsule Key', 'eSports Key']
update_prefix_remaining(types['keys'])

types['case'] = [prefix for prefix in prefix_remaining if 'Case' in prefix]
update_prefix_remaining(types['case'])

types['viewer_pass'] = [prefix for prefix in prefix_remaining if 'Viewer Pass' in prefix]
update_prefix_remaining(types['viewer_pass'])

types['souvenir_packages'] = [prefix for prefix in prefix_remaining if 'Souvenir Package' in prefix]
update_prefix_remaining(types['souvenir_packages'])

date_range =[*range(2012,2022)]
date_range = [str(year) for year in date_range]
types['all_major_capsules'] = [prefix for prefix in prefix_remaining for year in date_range if year in prefix]
types['all_major_capsules']= types['all_major_capsules'] +['Autograph Capsule']
update_prefix_remaining(types['all_major_capsules'])

types['souvenir_skins'] = [prefix for prefix in prefix_remaining if 'Souvenir' in prefix]
update_prefix_remaining(types['souvenir_skins'])

types['sticker_capsules'] = [prefix for prefix in prefix_remaining if 'Capsule' in prefix]
update_prefix_remaining(types['sticker_capsules'])

types['graffity'] = [prefix for prefix in prefix_remaining if 'Graffiti Box' in prefix]
types['graffity'] = types['graffity'] +['Sealed Graffiti']
update_prefix_remaining(types['graffity'])

types['patches'] = [prefix for prefix in prefix_remaining if 'Patch' in prefix]
update_prefix_remaining(types['patches'])

types['stickers'] = ['Sticker']
update_prefix_remaining(types['stickers'])

types['operation_pass'] = [prefix for prefix in prefix_remaining if 'Pass' in prefix]
update_prefix_remaining(types['operation_pass'])

types['junk'] =[prefix for prefix in prefix_remaining for aux in ['Music Kit','Name Tag','Pallet' ,'Parcel', 'Package'] if aux in prefix]
update_prefix_remaining(types['junk'])

types['agents'] = prefix_remaining.copy()
update_prefix_remaining(types['agents'])

all_types = list(types.keys())

def assing_type(skin):
    skin = skin.split('|')[0]
    skin = skin.rstrip().lstrip()
    for key, value in types.items():
        if skin in value:
            return str(key)
    
    return ''

df_overall_data['type'] =df_overall_data['itemName'].apply(assing_type)


def fig01_mean_price():
    mean = [df_price.iloc[i].mean() for i in range(len(df_price))]
    df_mean = pd.DataFrame(data = mean, columns=['price'], index = df_price.index)
    fig = px.line(df_mean, y = 'price', title = 'Media dos preços dos itens vendidos na data')
    fig.write_html("figs_html/fig01_mean_price.html")
    return

def fig01_median_price():
    median = [df_price.iloc[i].median() for i in range(len(df_price))]
    df_median = pd.DataFrame(data = median, columns=['price'], index = df_price.index)
    fig = px.line(df_median, y = 'price', title = 'Mediana dos preços dos itens vendidos na data')
    fig.write_html("figs_html/fig01_median_price.html")
    return

def fig01_mean_volume():
    mean = [df_vol.iloc[i].mean() for i in range(len(df_vol))]
    df_mean = pd.DataFrame(data = mean, columns=['price'], index = df_vol.index)
    fig = px.line(df_mean, y = 'price', title = 'Media do volume de itens vendidos na data')
    fig.write_html("figs_html/fig01_mean_price.html")
    return

def fig01_median_vol():
    median = [df_vol.iloc[i].median() for i in range(len(df_vol))]
    df_median = pd.DataFrame(data = median, columns=['price'], index = df_vol.index)
    fig = px.line(df_median, y = 'price', title = 'Mediana do volume de itens vendidos na data')
    fig.write_html("figs_html/fig01_median_price.html")
    return


def slope_after_44days():
    slope = []
    for i in range(len(df_overall_data)):
        skin = df_overall_data['itemName'].iloc[i]
        itemPrices = df_price[skin][df_price[skin].notnull()]
        #itemPrices ignorando primeiros 44 dias
        itemPrices = itemPrices[44:]
        if len(itemPrices) == 0:
            slope.append(np.nan)
            continue
        
        normTime = list(range(0,len(itemPrices)))
        fitR = sci.linregress(normTime,itemPrices)
        
        slope.append(fitR[0])
    type_column = df_overall_data['type']
    df = {
        'slope': slope,
        'type': type_column
        }
    df_slope = pd.DataFrame(data = df, index = df_overall_data.index)
    return df_slope
    
df_slope = slope_after_44days()

#media da inclinação da reta por grupo
def fig02_mean():
    slope = df_overall_data['slope'].groupby(df_overall_data['type']).mean().sort_values(ascending=False)
    fig = px.bar(slope, title="Média do Slope por grupo de items")
    fig.write_html("figs_html/fig02_mean.html")
    return

#mediana da inclinação da reta por grupo
def fig02_median():
    slope = df_overall_data['slope'].groupby(df_overall_data['type']).median().sort_values(ascending=False)
    fig = px.bar(slope, title="Mediana do Slope por grupo de items")
    fig.write_html("figs_html/fig02_median.html")
    return

#media da inclinação da reta por grupo
def fig02_mean():
    slope = df_slope['slope'].groupby(df_slope['type']).mean().sort_values(ascending=False)
    fig = px.bar(slope, title="Média do Slope por grupo de items ignorando os primeiros 44 dias")
    fig.write_html("figs_html/fig02_mean_44days.html")
    return

#mediana da inclinação da reta por grupo
def fig02_median():
    slope = df_slope['slope'].groupby(df_slope['type']).median().sort_values(ascending=False)
    fig = px.bar(slope, title="Mediana do Slope por grupo de items ignorando os primeiros 44 dias")
    fig.write_html("figs_html/fig02_median_44days.html")
    return

#box plot todos os tipos de itens
def fig03():
    medians = {}
    order =  []
    for type_ in list(df_overall_data['type'].unique()):
        median = df_overall_data['priceAvg'].where(df_overall_data['type'] == type_).dropna().median()
        medians[type_] = median
    order = [w for w in sorted(medians, key=medians.get ,reverse = True)]

    #ordenado pelo valro da mediana
    fig = px.box(df_overall_data, x = 'type', y='priceAvg', title ="Box plot dos preços por tipo de itens, y na escala logaritmica", category_orders={"type":order})
    fig.update_yaxes(type='log', dtick = 1)
    fig.write_html("figs_html/fig03.html")
    return

#box plot das armas
def fig04():
    medians = {}
    order =  []
    for type_ in ['ars','snipers', 'pistols','smgs', 'heavys']:
        median = df_overall_data['priceAvg'].where(df_overall_data['type'] == type_).dropna().median()
        medians[type_] = median

    order = [w for w in sorted(medians, key=medians.get ,reverse = True)]

    df_weapons = df_overall_data.loc[(df_overall_data['type'] == 'ars') | (df_overall_data['type'] == 'snipers') | (df_overall_data['type'] =='pistols') | (df_overall_data['type'] == 'smgs') | (df_overall_data['type'] == 'heavys')]
    fig = px.box(df_weapons, x = 'type', y='priceAvg',title="Box plot dos preços para as skins de armas", category_orders={"type":order})
    fig.update_yaxes(type='log', dtick = 1)
    fig.write_html("figs_html/fig04.html")
    return


def assing_glove_type(skin):
    skin = skin.split('|')[0]
    skin = skin.rstrip().lstrip()
    for tipo in types['gloves']:
        if skin == tipo:
            return str(tipo)
    
    return ''

b = df_overall_data.copy()
b['glove_type'] =df_overall_data['itemName'].apply(assing_glove_type)
b = b.where(b['glove_type'] != "").dropna()

#Box plot dos preços para skins de luvas
def fig05():
    medians = {}
    order =  []
    for type_ in types['gloves']:
        median = b['priceAvg'].where(b['glove_type'] == type_).dropna().median()
        medians[type_] = median

    order = [w for w in sorted(medians, key=medians.get ,reverse = True)]

    fig = px.box(b, x = 'glove_type', y='priceAvg',title="Box plot dos preços para skins de luvas", category_orders={"glove_type":order})
    fig.write_html("figs_html/fig05.html")
    return

#"Preço das caixas ao longo do tempo")
def fig06():
    cases_columns = [skin for skin in all_skins for prefix in types['case'] if prefix == skin.split('|')[0].lstrip().rstrip()]
    df_cases = df_price[cases_columns]

    fig = px.line(df_cases, y = cases_columns, title="Preço das caixas ao longo do tempo")
    fig.write_html("figs_html/fig06.html")
    return

#Preço dos adesivos Legends(Holo-Foil) ao longo do tempo")
legends_columns = [skin for skin in all_skins if 'Legends' in skin.split('|')[0].lstrip().rstrip() and
                        'Autograph' not in skin.split('|')[0].lstrip().rstrip() and
                        '2020' not in skin.split('|')[0].lstrip().rstrip()]
def fig07():
    fig = px.line(df_price, y = legends_columns ,title ="Preço dos adesivos Legends(Holo-Foil) ao longo do tempo")
    fig.write_html("figs_html/fig07.html")
    return


##adicionando as colunas %gain e %gainOneYear
for i in range(len(df_overall_data)):
    skin = df_overall_data['itemName'].iloc[i]
    itemPrices = df_price[skin][df_price[skin].notnull()]
    
    if skin in legends_columns:
        df_overall_data.at[i, '%gain']  = itemPrices[-1]/5 # 5 é o preço que as capsulas holo-foil vendem na loja
        continue
    else:
        if len(itemPrices) <= 30:
            df_overall_data.at[i, '%gain']  = np.nan
             
    #itemPrices ignorando primeiros 44 dias
    itemPrices = itemPrices[44:]
    
    if len(itemPrices) == 0:
        df_overall_data.at[i, '%gain']  = np.nan
        continue
    
    df_overall_data.at[i, '%gain'] = itemPrices[-1]/itemPrices[0]


for j in range(len(df_overall_data)):
    skin = df_overall_data['itemName'].iloc[j]
    itemPrices = df_price[skin][df_price[skin].notnull()]
    startDate = None
    
    if skin in legends_columns:
        startPrice = itemPrices[0]
        for i in range(len(itemPrices)):
            if itemPrices[i] <= startPrice * 0.75:
                startPrice = itemPrices[i]
                startDate = itemPrices.index[i]
                break
                
        if startDate == None:
            df_overall_data.at[j, '%gainOneYear']  = np.nan
            continue
    else:
        #itemPrices ignorando primeiros 44 dias
        itemPrices = itemPrices[44:]
        
        if len(itemPrices) == 0:
            df_overall_data.at[j, '%gainOneYear']  = np.nan
            continue
            
        startPrice = itemPrices[0]
        startDate = itemPrices.index[0]

    
    endDate = startDate + relativedelta(years=1)

    endPrice = None

    for i in range(len(itemPrices)):
        if itemPrices.index[i] > endDate:
            i = i -1
            endPrice = itemPrices[i]
            break

    if endPrice == None:
        df_overall_data.at[j, '%gainOneYear']  = np.nan
        continue
        

    df_overall_data.at[j, '%gainOneYear']  = (endPrice/ startPrice) - 1


#plot do %gainOneYear
# def fig08():
#     order = df_overall_data['%gainOneYear'].groupby(df_overall_data['type']).median().sort_values(ascending=False)
#     order = list(order.index)

#     fig = px.box(df_overall_data, x = 'type', y = '%gainOneYear', category_orders={"type":order})
#     fig.update_yaxes(type='log', dtick = 1)
#     fig.write_html("figs_html/fig08")
#     return

#"Média do %gainOneYear por grupo")
def fig08_mean():
    gainOneYear = df_overall_data['%gainOneYear'].groupby(df_overall_data['type']).mean().sort_values(ascending=False)
    fig = px.bar(gainOneYear, title="Média do %gainOneYear por grupo")
    fig.write_html("figs_html/fig08_mean.html")
    return

def fig08_median():
    gainOneYear = df_overall_data['%gainOneYear'].groupby(df_overall_data['type']).median().sort_values(ascending=False)
    fig = px.bar(gainOneYear, title="Mediana do %gainOneYear por grupo")
    fig.write_html("figs_html/fig08_median.html")
    return

df_legends = df_price[legends_columns]

data = {}
for skin in df_legends:
    prices = df_legends[skin].loc[df_legends[skin].first_valid_index():]
    prices = list(prices)
    prices = prices[0:365]
    data[skin] = prices
df = pd.DataFrame(data)

#"Radar chart dos preços dos adesivos"
def fig09():
    fig = go.Figure()
    for skin in df:
        fig.add_trace(go.Scatterpolar(
            r = df[skin], 
            theta = df.index,
            name = skin
        ))
    fig.update_layout(title="Radar chart dos preços dos adesivos" )
    fig.write_html("figs_html/fig09.html")
    return

# fig01_mean_price()
# fig01_median_price()
# fig01_mean_volume()
# fig01_median_vol()

# fig02_mean()
# fig02_median()

# fig03()
# fig04()
# fig05()
# fig06()
# fig07()
# fig08_mean()
# fig08_median()
fig09()

