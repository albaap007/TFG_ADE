import csv
from instaloader import Instaloader, Profile
from datetime import datetime
from datetime import timedelta
from itertools import dropwhile, takewhile
from os import listdir, mkdir
import os


def get_data_influencers (csv_file):

    L = Instaloader( compress_json=False, save_metadata=False )  

   # archivo csv
    campos_csv = ['num', 'username', 'full_name','business','verified','bio','category','followers','followees','nPost','nIgtv', 'reels']
    lista_filas = []
    
    with open(csv_file, newline='') as File:  
        reader = csv.reader(File)
        for row in reader:
            str_profile = row[0]
            a =  str_profile.split(sep =';')               
            profile = Profile.from_username(L.context, a[0])

            # preparamos la tabla resumen
            fila = {}
            fila['num'] = 0
            fila['username'] = a[0]
            fila['full_name'] = profile.full_name
            if profile.is_business_account:
                fila['business'] = 1

            else:
                fila['business'] = 0
            
            if profile.is_verified:
                fila['verified'] = 1

            else:
                fila['verified'] = 0
            
            fila['bio'] = profile.biography.replace('\n', ' ').replace('\r', ' ')
            fila ['category'] = profile.business_category_name
            fila['followers'] = profile.followers
            fila['followees'] = profile.followees
            fila['nPost'] = profile.mediacount
            fila ['nIgtv'] = profile.igtvcount
            if profile.has_highlight_reels:
                fila['reels'] = 1

            else:
                fila['reels'] = 0
            print(a[0])

            lista_filas.append(fila)


    # actualizamos el índice de los posts
    for n_fila, fila in enumerate(reversed(lista_filas)):
        fila['num'] = n_fila + 1

    # guardamos el resumen
    with open(str_directorio + '/0_' + 'lista_influencers' + '_resumen.csv', 'w', encoding='UTF-16') as archivo:
        writer = csv.DictWriter(archivo, fieldnames=campos_csv, delimiter='\t')
        writer.writeheader()
        writer.writerows(reversed(lista_filas))

str_directorio = '/Users/albaprimoaparici/Desktop/TFG'
print('OPERACIÓN INICIADA')
followers = get_data_influencers('lista_influencers.csv')
print('OPERACIÓN FINALIZDA')