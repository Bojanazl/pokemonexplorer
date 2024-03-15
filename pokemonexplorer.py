import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import requests

#st.set_page_config( layout='wide') #wide page view

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

local_css("style.css")

#containers
header = st.container(height=None, border=True)
choice = st.container(height=None, border=True)
features = st.container(height=None, border=True)
comparison = st.container(border=True)


def get_pokemon_names():
    try:
        url = "https://pokeapi.co/api/v2/pokemon?limit=1000"
        response = requests.get(url)
        data = response.json()
        pokemon_names = [pokemon['name'] for pokemon in data['results']]
        return pokemon_names
    except:
        return np.NAN

def get_pokemon_details(pokemon_name):
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
        response = requests.get(url)
        pokemon_data = response.json()

        name = pokemon_data['name']
        height = pokemon_data['height']
        weight = pokemon_data['weight']
        moves = len(pokemon_data['moves'])
        image_url = pokemon_data['sprites']['other']['official-artwork']['front_default']
        cry = pokemon_data['cries']['latest']
        cry_legacy = pokemon_data['cries']['legacy']

        return name, height, weight, moves, image_url, cry, cry_legacy
    except:
        return np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN


#title form
with header:
      st.title("Pokemon Explorer")
      st.text("Welcome to Pokemon Explorer. Select your Pokemon to find out more about them!")

pokemon_names = get_pokemon_names()

#choosing form
with choice:
    st.header("Choose your Pokemon:")
    first_pokemon = st.selectbox("", pokemon_names, key = "pokemon_1")
    if first_pokemon:
            st.write("You have chosen:", first_pokemon.capitalize())

#features form
with features:
    st.header("Pokemon details:")
    
    if first_pokemon:
        name, height, weight, moves, image_url, cry, cry_legacy = get_pokemon_details(first_pokemon)
        if name:
                col1, col2 = st.columns(2)

                #column1
                with col1:
                    st.write(f"**Name: {name.capitalize()}**")
                    st.write(f"**Height:** {height}")
                    st.write(f"**Weight:** {weight}")
                    st.write(f"**Number of Moves:** {moves}")

                    #latest battle cry
                    if cry:
                        st.write("")
                        st.write("**Latest Battle Cry:**")
                        st.audio(cry, format='audio/ogg')
                        st.write("")
                    else:
                        st.write("Something happened to battlecry: cannot be found!")
                    
                    #legacy battle cry
                    if cry_legacy:
                         st.write("**Legacy Battle Cry:**")
                         st.audio(cry_legacy, format='audio/ogg')

                #column 2
                with col2:
                    if image_url:
                        st.image(image_url, caption=name.capitalize(), use_column_width=True, width = 100)
        else:
            st.write("Something went wrong! Who is that Pokemon?")


#comparison form 
with comparison:
    st.header("Choose another Pokemon to compare to " +first_pokemon.capitalize())
    second_pokemon = st.selectbox("", get_pokemon_names(), key = "pokemon_2")

    name_1, height_1, weight_1, moves_1, image_url_1, cry_1, cry_legacy_1  = get_pokemon_details(first_pokemon)
    name_2, height_2, weight_2, moves_2, image_url_2, cry_2, cry_legacy_2 = get_pokemon_details(second_pokemon)

    col1, col2 = st.columns(2)
    #column 1
    with col1:
        #this should be in a different file :(
            st.write(f"**Name:** {name.capitalize()}")
            st.write(f"Number of moves for: {moves_1}")
            if image_url_2:
                st.image(image_url_1, caption= first_pokemon.capitalize(), use_column_width=True, width = 100)
    #column 2
    with col2:
            st.write(f"**Name:** {name_2.capitalize()}")
            st.write(f"**Number of moves for**: {moves_2}")
            if image_url_2:
                st.image(image_url_2, caption= second_pokemon.capitalize(), use_column_width=True, width = 100)

    #diagram in a new container
    plot = st.container(border=True)

    with plot:
        if height_1 is not None and height_2 is not None:
             st.header("Diagram:")

        fig, axs = plt.subplots(1, 2, figsize=(15, 5))

        height_colours = ['#60f3586f', '#9400fd5f']
        weight_colours = ['#60f3586f', '#9400fd5f']

        #height of a pokemon
        axs[0].bar([first_pokemon.capitalize(), second_pokemon.capitalize()], [height_1, height_2], color=height_colours)
        axs[0].set_title("Height Comparison")
        axs[0].set_ylabel("Height in dm")

        #weight of a pokemon
        axs[1].bar([first_pokemon.capitalize(), second_pokemon.capitalize()], [weight_1, weight_2], color=weight_colours)
        axs[1].set_title("Weight Comparison")
        axs[1].set_ylabel("Weight in kg")

        st.pyplot(fig)

