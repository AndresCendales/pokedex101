import requests
from bs4 import BeautifulSoup
import pandas as pd

url_national_pokedex = 'https://serebii.net/pokemon/nationalpokedex.shtml'
page_response = requests.get(url_national_pokedex)  
s_page_response = BeautifulSoup(page_response.content,'html.parser')

pokemon_rows = s_page_response.find('table', attrs={'align':'center','class':'dextable'}).find_all('tr')

def resolve_type_pokemon(type_pokemon_list):
    resolve_list = []
    for type_pokemon in type_pokemon_list:
        url_type_pokemon =  type_pokemon.get('href')
        resolve_type = url_type_pokemon.replace('/pokemon/type/','')
        resolve_list.append(resolve_type)
    return resolve_list


def obtener_data_total():
    data_set =[]
    for pokemon in pokemon_rows[2:1787:2]:
        pokemon_data = pokemon.find_all('td')

        #Diccionario que guardara toda la informacion general de los pokemon 
        pokemon_dict = {}
        resolve_List = []
        habilidades = []

        #Numero del pokemon en la pokedex
        numero = pokemon_data[0].get_text()
        pokemon_dict['pokemon_number'] = numero[5:8]
        
        # image_url
        

        #Icono del pokemon
        pokemon_dict['icon_url'] = 'https://serebii.net' +  pokemon_data[2].img.get('src')

        #Nombre del pokemon en Ingles
        pokemon_dict['english_name'] = pokemon_data[3].a.get_text()

        #Tipo de pokemon
        resolve_List = resolve_type_pokemon(pokemon_data[4].find_all('a'))
        pokemon_dict['type_1'] = resolve_List[0]
        if len(resolve_List) >1:
            pokemon_dict['tipe_2'] = resolve_List[1]
        else:
            pokemon_dict['tipe_2'] = None

        #Habilidades de los pokemon
        habilidades = [ability.get_text() for ability in pokemon_data[5].find_all('a') ]
        pokemon_dict['abilities_1'] = habilidades[0]
        
        if len(habilidades) == 2:
            pokemon_dict['abilities_2'] = habilidades[1]
            pokemon_dict['abilities_3'] = None
        elif len(habilidades) == 3:
            pokemon_dict['abilities_2'] = habilidades[1]
            pokemon_dict['abilities_3'] = habilidades[2]
        else:
            pokemon_dict['abilities_2'] = None
            pokemon_dict['abilities_3'] = None
        
        #Experiencia

        #Generation
        
        #Ataque
        pokemon_dict['attack'] = pokemon_data[7].get_text()

        #Ataque especial
        pokemon_dict['special_att'] = pokemon_data[9].get_text()

        #defensa
        pokemon_dict['defense'] = pokemon_data[8].get_text()

        #special defense
        pokemon_dict['special_defense'] = pokemon_data[10].get_text()

        #Velociadad
        pokemon_dict['speed'] = pokemon_data[11].get_text()

        #HP
        pokemon_dict['hp'] = pokemon_data[6].get_text()

        #weight__kg
        
        #height_m

        #percentage_male

        #percentage_female

        print('Se ha guardado el pokemon {} - {}'.format(pokemon_dict['pokemon_number'],pokemon_dict['english_name']))
        data_set.append(pokemon_dict)
    return(data_set)

def obtener_url_individual():
    urls_imagenes = {}
    for pokemon in pokemon_rows[2:1787:2]:
        pokemon_data = pokemon.find_all('td')
        
        #Numero del pokemon en la pokedex
        numero = pokemon_data[0].get_text()
        numero = numero[5:8] 

        #url de la pagina principal del pokemon individual
        url = 'https://serebii.net' + pokemon_data[1].a.get('href')
        
        #guardar en el diccionario de urls
        urls_imagenes[numero] = url 
        
    return urls_imagenes





def save_data(data):
    df = pd.DataFrame(data)
    df.to_csv('pokemones_general.csv')
    print('Guadrado')
    return df


if __name__ == "__main__":
    urls_imagenes = obtener_url_individual()
    # resultado = obtener_data_total()


