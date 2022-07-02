import csv
from instaloader import Instaloader, Profile
from datetime import datetime
from datetime import timedelta
from itertools import dropwhile, takewhile
from os import listdir, mkdir
import pandas as pd


# periodo a descargar: AMBAS FECHAS INCLUIDAS
INICIO = datetime(2021, 1, 1)
FINAL = datetime(2021, 12, 31)
XD =datetime(2021, 12, 31)

#preparo dataframe para actualizar csv con la lista de usuarios
df = pd.read_csv("lista.csv", sep= ';', engine='python', on_bad_lines='skip')
print(df.columns)
dfs = df[['User','Proc']]
#A05P12A98vpnz
results = []
shortid = []
fecha = []
#archivo CSV doonde guardo los datos
str_directorio = '/Users/albaprimoaparici/Desktop/dataset'
campos_csv = ['num', 'post', 'shortcode', 'user','fecha', 'hora', 'tipoPost', 'mediacount', 'likes', 'comentarios',
                  'texto', 'hashtags', 'sponsored', 'sponsor', 'menciones', 'etiquetas', 'videoView', 'videoTime']
 
def reanudo_descarga (csv_file):
    
    with open(csv_file, newline='') as File:  
        reader = csv.reader(File, delimiter=';')
        next(reader, None)
        print ("Iniciamos sesion")
        L = Instaloader( compress_json=False, save_metadata=False )         # no queremos la información sobre el nodo de Instagram
        L.interactive_login("albaap007")
        #fjeronimagales  tfgdatabase

        for row in reader:
            #a = row[0]
            #a.split(sep =';') 
            str_profile = row[1]
            proc = row[2]

            print (str_profile + ' ---- ' + proc)

            if str_profile not in listdir('.'):
                    mkdir(str_profile)
                    #descarga estandar
                    descarga_e(L, str_profile, INICIO, FINAL)
                    dfs.loc[dfs['User'] == str_profile, 'Proc'] = '1'
                    dfs.to_csv('lista.csv', sep=';')
                
            else:
                if (proc != '1') :
                    print('vale, hemos entrado aquí')
                    with open('0_dataset_resumen_c.csv', 'r') as File:
                        reader = csv.reader(File, delimiter=';')
                        # Omitir el encabezado
                        next(reader, None)
                       # for row in reader:
                        #    results.append(row)
                         #   shortid.append(row[2])
                          #  fecha.append(row[4])

                        #res = list(reversed(results))
                       # lastRow = res[0]
                        #fechaUlt = lastRow[4]   
                        #fechaUlt_dt = datetime.strptime(fechaUlt, '%Y-%m-%d')
                        #print(fechaUlt_dt)
                        #descarga excepcional
                        descarga_x(L, str_profile,INICIO,XD,shortid)

                        dfs.loc[dfs['User'] == str_profile, 'Proc'] = '1'
                        dfs.to_csv('lista.csv', sep=';')

    
   # with open( str_directorio +'/0_' + 'dataset' + '_resumen_1.csv', 'a', encoding='UTF-8') as archivo:
      #  writer = csv.DictWriter(archivo, fieldnames=campos_csv, delimiter='\t')

def descarga_e(L, str_profile, dt_fecha_inicio, dt_fecha_final):

    print('Empiezo descarga') 
    # L = Instaloader( compress_json=False, save_metadata=False )         # no queremos la información sobre el nodo de Instagram
    print('instaloader')
    profile = Profile.from_username(L.context, str_profile)
    print('profile')
    posts = profile.get_posts()
    print('get posts')
    n = 0

    lista_filas = []

    with open( str_directorio +'/0_' + 'dataset' + '_resumen_c.csv', 'a', encoding='UTF-8') as archivo:
        writer = csv.DictWriter(archivo, fieldnames=campos_csv, delimiter=';')

        for post in takewhile(lambda p: p.date > dt_fecha_inicio, dropwhile(lambda p: p.date > dt_fecha_final  + timedelta(1), posts)):

            # grabamos el post
            L.download_post( post, str_profile )

            # incrementamos el contador
            n += 1

            # preparamos la tabla resumen
            fila = {}
            fila['num'] = n                                                 # posteriormente lo actualizamos
            fila['post'] =  post.date.strftime('%Y-%m-%d_%H-%M-%S_UTC')
            fila['shortcode'] = post.shortcode
            fila['user'] = post.owner_username
            # ajustamos la hora de UTC a horario en España
            dt_post_corregido = post.date + timedelta(hours=1)
            fila['fecha'] = dt_post_corregido.strftime('%Y-%m-%d')
            fila['hora'] = dt_post_corregido.strftime('%H:%M:%S')
            fila ['tipoPost'] = post.typename
            fila['mediacount'] = post.mediacount
            fila['likes'] = post.likes
            fila['comentarios'] = post.comments
            if (post.caption == 'NoneType'):
                fila['texto'] = 'NoneType'
            else:
                fila['texto'] = post.caption.replace('\n', ' ').replace('\r', ' ')

            fila['hashtags'] = '; '.join(list(set(post.caption_hashtags)))
                            
            if post.is_sponsored:
                fila['sponsored'] = 1
                fila['sponsor'] = 'BUSCAR' #'; '.join(list(set(post.sponsor_users))) #devuelve una lista de objetos Profile
            
            else:
                fila['sponsored'] = 0
                fila['sponsor'] = 'n/p'

            fila['menciones'] = '; '.join(list(set(post.caption_mentions)))
            fila['etiquetas'] = '; '.join(list(set(post.tagged_users)))
            fila['videoView'] = post.video_view_count
            fila ['videoTime'] = post.video_duration

            archivo.write('\n')
            writer.writerow(fila)
            lista_filas.append(fila)

    print ( 'Usuario ' + str_profile + ' descargado al completo ' )

def descarga_x(L, str_profile, dt_fecha_inicio, dt_fecha_final, shortid):

    print('Empiezo descarga')
    # L = Instaloader( compress_json=False, save_metadata=False )         # no queremos la información sobre el nodo de Instagram
    # L.interactive_login("fjeronimagales")
    print('instaloader')
    profile = Profile.from_username(L.context, str_profile)
    print('profile')

    posts = profile.get_posts()
    print('get posts')

    n = 0

    lista_filas = []

    with open( str_directorio +'/0_' + 'dataset' + '_resumen_c.csv', 'a', encoding='UTF-8') as archivo:
        writer = csv.DictWriter(archivo, fieldnames=campos_csv, delimiter=';')

        for post in takewhile(lambda p: p.date > dt_fecha_inicio, dropwhile(lambda p: p.date > dt_fecha_final  + timedelta(1), posts)):
            #if post.shortcode not in shortid:
                # grabamos el post
            
            L.download_post( post, str_profile )
            

                # incrementamos el contador
            n += 1

                # preparamos la tabla resumen
            fila = {}
            fila['num'] = n                                                 # posteriormente lo actualizamos
            fila['post'] =  post.date.strftime('%Y-%m-%d_%H-%M-%S_UTC')
            fila['shortcode'] = post.shortcode
            fila['user'] = post.owner_username
            # ajustamos la hora de UTC a horario en España
            dt_post_corregido = post.date + timedelta(hours=1)
            fila['fecha'] = dt_post_corregido.strftime('%Y-%m-%d')
            fila['hora'] = dt_post_corregido.strftime('%H:%M:%S')
            fila ['tipoPost'] = post.typename
            fila['mediacount'] = post.mediacount
            fila['likes'] = post.likes
            fila['comentarios'] = post.comments
            if (post.caption == 'NoneType'):
                fila['texto'] = 'NoneType'
            else:
                fila['texto'] = post.caption.replace('\n', ' ').replace('\r', ' ')

            #fila['texto'] = post.caption.replace('\n', ' ').replace('\r', ' ').replace(';', ',')
            fila['hashtags'] = '; '.join(list(set(post.caption_hashtags)))
                            
            if post.is_sponsored:
                fila['sponsored'] = 1
                fila['sponsor'] = 'BUSCAR'#'; '.join(list(set(post.sponsor_users))) #devuelve una lista de objetos Profile
            
            else:
                fila['sponsored'] = 0
                fila['sponsor'] = 'n/p'

            fila['menciones'] = '; '.join(list(set(post.caption_mentions)))
            fila['etiquetas'] = '; '.join(list(set(post.tagged_users)))
            fila['videoView'] = post.video_view_count
            fila ['videoTime'] = post.video_duration

            archivo.write('\n')
            writer.writerow(fila)
            lista_filas.append(fila)
            #else:    
                #print ('Post ' + post.shortcode + ' ya existe.')

    print ( 'Usuario ' + str_profile + ' descargado al completo ' )

print('Empiezo proceso de descarga...')
reanudo_descarga('lista.csv')