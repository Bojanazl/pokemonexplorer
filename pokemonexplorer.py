import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns 
import pandas as pd
import requests

st.title("Pokemon Explorer!")

def get_details(poke_number):
	try:
		url = f'https://pokeapi.co/api/v2/pokemon/{poke_number}/'
		response = requests.get(url)
		pokemon = response.json()
		return pokemon['name'], pokemon['height'], pokemon['weight'], len(pokemon['moves']), pokemon['sprites']['front_default'], pokemon['cries']['latest']
	except:
		return 'Error', np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN

#slider
st.header("Pick a pokemon: ")
pokemon_number = st.slider("Slide:",
						   min_value=1,
						   max_value=150
						   )

name, height, weight, moves, image_url, cry = get_details(pokemon_number)


#columns
col1, col2, col3 = st.columns(3)

#pokemon info
with col1:
    st.write(f'**Name:** {name.title()}')
    st.write(f'**Height:** {height}cm')
    st.write(f'**Weight:** {weight}')
    st.write(f'**Move Count:** {moves}')
	
#image
with col2:
	st.text("Pokemon looks:")
	st.image(image_url, caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

#audio
with col3:
    st.text("Pokemon Cry:")
    st.audio(cry, format='audio/ogg')
	

#chart
#colour_types = {'normal' :'gray',
#                'fire': 'red',
#                'water': 'dodgerblue',
#                'electric': 'yellow',
#                'grass': 'limegreen',
#                'ice': 'lightblue',
#                'fighting': 'sienna',
#                'poison': 'mediumorchid',
#                'ground': 'goldenrod',
#                'flying': 'cornflowerblue',
#                'psychic': 'hotpink',
#                'bug': 'yellowgreen',
#                'rock': 'darkkhaki',
#                'ghost': 'slateblue',
#                'dragon': 'mediumpurple',
#                'dark': 'saddlebrown',
#                'steel': 'darkgray',
#                'fairy': 'violet'}


#height_data = pd.DataFrame ({'Pokemon': ['Weedle', name.title(), 'Victreebel'],'Heights': [2, height, 17]})
#colors = ['gray', 'red', 'gray']
#graph = sns.barplot(data = height_data, 
#					x = 'Pokemon', 
#					y = 'Heights', 
#					palette = colors)

#st.pyplot(graph.figure)




