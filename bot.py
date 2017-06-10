# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import json
#el link de la pagina es http://www.ecovehiculos.gob.mx/buscamarcamodelo.php
#Se que la pagina tiene 48 marcas de vehiculos en la cual pretendo iterar, por eso creo una lista con 48 elementos para iterar en las marcas
limite1= 48
x=range(limite1)
#Al iterar en la pagina estas sujeto a que falle por erroes de la misma pagina, es por eso que tambien se puede expecificar el numero de la marca en la cueal se desea iterar, un ejemplo es 13 dandonos ford o 16 honda
#x=[13,16,20,47]
driver = webdriver.Chrome()
for i in x:
    #Entra a la pagina
    driver.get('http://www.ecovehiculos.gob.mx/buscamarcamodelo.php')
    time.sleep(1)
    #itera sobre marcas-----------------------------------------------------------------------
    if 0 < i:
        #suma uno a i por la estructura del dropdown menu siendo 1 un elemento vacio, por lo tanto 2 es ACURA ....
        i+=1
        marca = driver.find_element_by_xpath("/html/body/table/tbody/tr[4]/td/table/tbody/tr/td[2]/table[2]/tbody/tr/td/form/select[1]/option["+str(i)+"]")
        #Esto puede ser utilizado para darle la marca en el json, guarda la marca a consultar
        keymarca= marca.text
        print keymarca
        marca.click()
        #abre el json para agregar como key la marca
        with open('json.json','r') as file:
            son =json.load(file)
            #print son
            son["Marca"][keymarca]={}
        with open('json.json','w') as file:
            json.dump(son, file)

        #obtiene el numero de opciones del dropdown menu, siendo ahora submarcas
        modelo= driver.find_element_by_name('vehiculo_submarca')
        opciones_modelo=modelo.find_elements_by_tag_name('option')
        limite2= len(opciones_modelo)
        #itera sobre submarcas----------------------------------------------------------------------------
        for j in range(limite2):
            if 0 < j:
                j+=1
                modelo = driver.find_element_by_xpath("/html/body/table/tbody/tr[4]/td/table/tbody/tr/td[2]/table[2]/tbody/tr/td/form/select[2]/option["+str(j)+"]")
                #Esto puede ser utilizado para darle la submarca a consultar en el json
                keymodelo= modelo.get_attribute('value')
                print keymodelo
                modelo.click()
                #abre el json para agregar dentro del diccionario de la marca una key con la submarca
                with open('json.json','r') as file:
                    son =json.load(file)

                    son["Marca"][keymarca][keymodelo]={}
                with open('json.json','w') as file:
                    json.dump(son, file)
                #obtiene el numero de opciones del dropdown menu, siendo ahora modelos(anios)
                ano= driver.find_element_by_name('vehiculo_modelo')
                opciones_ano=ano.find_elements_by_tag_name('option')
                limite3= len(opciones_ano)
                #itera sobre modelos(anios)-------------------------------------------------------
                for k in range(limite3):
                    k+=1
                    ano = driver.find_element_by_xpath("/html/body/table/tbody/tr[4]/td/table/tbody/tr/td[2]/table[2]/tbody/tr/td/form/select[3]/option["+str(k)+"]")
                    #Esto puede ser utilizado para darle el modelo a consultar en el json
                    keyano= ano.get_attribute('value')
                    print keyano
                    ano.click()
                    #abre el json para agregar dentro del diccionario de la submarca una key con el modelo
                    with open('json.json','r') as file:
                        son =json.load(file)

                        son["Marca"][keymarca][keymodelo][keyano]={}
                    with open('json.json','w') as file:
                        json.dump(son, file)

                    #valda para pasar a la siguiente pagina con una tabla sencilla, no siendo lo suficiente para los datos de los vehiculos
                    validar = driver.find_element_by_xpath("/html/body/table/tbody/tr[4]/td/table/tbody/tr/td[2]/table[2]/tbody/tr/td/form/a[2]/img")
                    validar.click()
                    time.sleep(2)
                    #obtiene la url en la cual estan los datos completos de las versiones mostradas en la segunda pagina; se mete a la direccione obtenida
                    link= driver.find_element_by_xpath("/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table[2]/tbody/tr/td/center/a")
                    tabla=link.get_attribute("href")
                    #Esto guarda un link el cual puede ser guardado en la api para ver la tabla
                    keytabla= tabla
                    print keytabla
                    driver.get(tabla)
                    #abre el json para agregar como key referencia y valor una url para la consulta de las tablas
                    with open('json.json','r') as file:
                        son =json.load(file)

                        son["Marca"][keymarca][keymodelo][keyano]['Referencia']=keytabla
                    with open('json.json','w') as file:
                        json.dump(son, file)

                    #En este punto se implementa la obtencion de los datos de la tabla
                    filas= driver.find_element_by_xpath('/html/body/table/tbody')
                    filast=driver.find_elements_by_tag_name('tr')
                    total_filas=len(filast)
                    #Esta parte es escencial para la constuccion del json,
                    #permite crear una lista de diccionarios en las cueles se ingresaran todas las versiones de un carro
                    with open('json.json','r') as file:
                        son =json.load(file)
                        son["Marca"][keymarca][keymodelo][keyano]['Versiones']=range(total_filas-1)
                    with open('json.json','w') as file:
                        json.dump(son, file)
                    #itera sobre el total de filas de las tablas para sacar los datos de esta de una forma ordenada
                    for l in range(total_filas):
                        if 0 < l:
                            l+=1
                            version = driver.find_element_by_xpath('/html/body/table/tbody/tr['+str(l)+']/td[3]')
                            version= version.text
                            transmision = driver.find_element_by_xpath('/html/body/table/tbody/tr['+str(l)+']/td[5]')
                            transmision= transmision.text
                            combustible = driver.find_element_by_xpath('/html/body/table/tbody/tr['+str(l)+']/td[6]')
                            combustible= combustible.text
                            cilindros = driver.find_element_by_xpath('/html/body/table/tbody/tr['+str(l)+']/td[7]')
                            cilindros= cilindros.text
                            potencia = driver.find_element_by_xpath('/html/body/table/tbody/tr['+str(l)+']/td[8]')
                            potencia= potencia.text
                            tamano = driver.find_element_by_xpath('/html/body/table/tbody/tr['+str(l)+']/td[9]')
                            tamano= tamano.text
                            categoria = driver.find_element_by_xpath('/html/body/table/tbody/tr['+str(l)+']/td[10]')
                            categoria= categoria.text
                            ren_ciudad = driver.find_element_by_xpath('/html/body/table/tbody/tr['+str(l)+']/td[11]')
                            ren_ciudad= ren_ciudad.text
                            ren_carretera = driver.find_element_by_xpath('/html/body/table/tbody/tr['+str(l)+']/td[12]')
                            ren_carretera= ren_carretera.text
                            ren_combinado = driver.find_element_by_xpath('/html/body/table/tbody/tr['+str(l)+']/td[13]')
                            ren_combinado= ren_combinado.text
                            ren_ajustado = driver.find_element_by_xpath('/html/body/table/tbody/tr['+str(l)+']/td[14]')
                            ren_ajustado= ren_ajustado.text
                            co2 = driver.find_element_by_xpath('/html/body/table/tbody/tr['+str(l)+']/td[15]')
                            co2= co2.text
                            nox = driver.find_element_by_xpath('/html/body/table/tbody/tr['+str(l)+']/td[16]')
                            nox= nox.text
                            cal_gas = driver.find_element_by_xpath('/html/body/table/tbody/tr['+str(l)+']/td[17]')
                            cal_gas= cal_gas.text
                            cal_cont = driver.find_element_by_xpath('/html/body/table/tbody/tr['+str(l)+']/td[18]')
                            cal_cont= cal_cont.text
                            #ya con todos los datos obtenidos abre el json y mete todos los datos en su respectivo key
                            with open('json.json','r') as file:
                                son =json.load(file)
                                son["Marca"][keymarca][keymodelo][keyano]['Versiones'][l-2]={}
                                son["Marca"][keymarca][keymodelo][keyano]['Versiones'][l-2]['Version']=version
                                son["Marca"][keymarca][keymodelo][keyano]['Versiones'][l-2]['Transmision']=transmision
                                son["Marca"][keymarca][keymodelo][keyano]['Versiones'][l-2]['Combustible']=combustible
                                son["Marca"][keymarca][keymodelo][keyano]['Versiones'][l-2]['Cilindros']=cilindros
                                son["Marca"][keymarca][keymodelo][keyano]['Versiones'][l-2]['Potencia']=potencia
                                son["Marca"][keymarca][keymodelo][keyano]['Versiones'][l-2]['Tamaño']=tamano
                                son["Marca"][keymarca][keymodelo][keyano]['Versiones'][l-2]['Categoria']=categoria
                                son["Marca"][keymarca][keymodelo][keyano]['Versiones'][l-2]['Rendimiento_ciudad']=ren_ciudad
                                son["Marca"][keymarca][keymodelo][keyano]['Versiones'][l-2]['Rendimiento_carretera']=ren_carretera
                                son["Marca"][keymarca][keymodelo][keyano]['Versiones'][l-2]['Rendimiento_combinado']=ren_combinado
                                son["Marca"][keymarca][keymodelo][keyano]['Versiones'][l-2]['Rendimiento_ajustado']=ren_ajustado
                                son["Marca"][keymarca][keymodelo][keyano]['Versiones'][l-2]['Co2']=co2
                                son["Marca"][keymarca][keymodelo][keyano]['Versiones'][l-2]['NOx']=nox
                                son["Marca"][keymarca][keymodelo][keyano]['Versiones'][l-2]['Calificacion_gas_efecto_invernadero']=cal_gas
                                son["Marca"][keymarca][keymodelo][keyano]['Versiones'][l-2]['Calificacion_gas_contaminante_aire']=cal_cont
                            with open('json.json','w') as file:
                                json.dump(son, file)


                    #vuelve a la pagina principal
                    #time.sleep(1)

                    driver.get('http://www.ecovehiculos.gob.mx/buscamarcamodelo.php')
                    #http://ecovehiculos.gob.mx/buscamarcamodelo.php? se cayo, ahora es http://www.ecovehiculos.gob.mx/buscamarcamodelo.php
                    marca = driver.find_element_by_xpath("/html/body/table/tbody/tr[4]/td/table/tbody/tr/td[2]/table[2]/tbody/tr/td/form/select[1]/option["+str(i)+"]")
                    print marca.text
                    marca.click()

                    modelo = driver.find_element_by_xpath("/html/body/table/tbody/tr[4]/td/table/tbody/tr/td[2]/table[2]/tbody/tr/td/form/select[2]/option["+str(j)+"]")
                    #Esto puede ser utilizado para darle la submarca a consultar en el json
                    print modelo.get_attribute('value')
                    modelo.click()

                    continue

                continue
#foma del json.json bacio
#{"Marca": {}}
