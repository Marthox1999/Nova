from django.test import TestCase
from inventario.models import *
from usuarios.models import *

#FUNCIÓN - PRIMERA PRUEBA
def bodegaconsulta(idBodega):
    categorias = Categoria.objects.all() #para cargar las categorias en el navbar
    bodegas = Bodega.objects.all()

    #modificar = request.POST

    if(idBodega=='-1' or idBodega==None):
        ciudadBodega = ""
        dirBodega = ""        
    else:
        BodegaObject = Bodega.objects.get(pkBodega=idBodega)
        ciudadBodega = BodegaObject.ciudad
        dirBodega = BodegaObject.direccion

    return {'idBodega':idBodega,'ciudadBodega':ciudadBodega,'dirBodega':dirBodega}


#FUNCIÓN - SEGUNDA PRUEBA
def duenioAdminIngreso(request, ingresar):
    categorias = Categoria.objects.all()
    context={'categorias':categorias}
    #ingresar = request.POST
    if(request.get('method') == 'POST'):
        admin = AdministradorDuenio(            
            nombreUsuario=ingresar.get('nombreUsuario'),
            clave=ingresar.get('clave'),
            tipo='ADMIN'
        )

        duenio=AdministradorDuenio(
            nombreUsuario=ingresar.get('nombreUsuario'),
            clave=ingresar.get('clave'),
            tipo='CEO'
        )
        nombre=ingresar.get('nombreDuenioAdmin')
        if (admin.autenticarAdmin()):
            #messages.success(request, f'¡Bienvenido {nombre}!')
            return "ADMIN"
        elif (duenio.autenticarDuenio()):            
            #messages.success(request, f'¡Bienvenido {nombre}!')
            return "DUENIO"
        else:
            #messages.info(request, 'Cuenta de usuario o contraseña invalida')
            return "INVALIDO"
    return "SEND"


#PRUEBAS
class PruebasFunciones(TestCase):

    def setUp(self):
        print("preparando contexto")
        #CONTEXTO FUNC 1
        self.bodega1 = Bodega(pkBodega=1,
                              direccion="1",
                              ciudad = "11").save()
        self.bodega1Datos = {'idBodega':1,'dirBodega':"1",'ciudadBodega':"11"}#if idBodega==1

        self.bodega2 = Bodega(pkBodega=2,
                              direccion="2",
                              ciudad = "22").save()
        self.bodega2Datos = {'idBodega':2,'dirBodega':"2",'ciudadBodega':"22"} #if idBodega==2

        self.bodega3Datos = {'idBodega':"-1",'dirBodega':"",'ciudadBodega':""} #if idBodega=="-1"
        self.bodega4Datos = {'idBodega':None,'dirBodega':"",'ciudadBodega':""} #if idBodega == None

        #CONTEXTO FUNC 2
        self.request1 = {'method':"POST"}#TRUE
        self.request2 = {'method':"SEND"}#FALSE

        self.duenio = AdministradorDuenio(pkAdministradorDuenio = 1,
                                          nombreUsuario="Duenio",
                                          clave="123",
                                          tipo="CEO").save()
        self.duenioDatos = {'nombreUsuario':"Duenio", 'clave':"123",'tipo':"CEO"}        

        self.admin = AdministradorDuenio(pkAdministradorDuenio = 2,
                                         nombreUsuario="Admin",
                                         clave="123",
                                         tipo="ADMIN").save()
        self.adminDatos = {'nombreUsuario':"Admin", 'clave':"123",'tipo':"ADMIN"}

        self.noUser = {'nombreUsuario':"user", 'clave':"0",'tipo':"Nada"}
    
    def test_bodegaConsulta(self):
        print("Realizando la primera prueba (bodegaConsulta)")
        self.assertEqual(bodegaconsulta(2), self.bodega2Datos)
        self.assertEqual(bodegaconsulta('-1'), self.bodega3Datos)
        self.assertEqual(bodegaconsulta(1), self.bodega1Datos)
        self.assertEqual(bodegaconsulta(None), self.bodega4Datos)

    def test_duenioAdminIngreso(self):
        print("Realizando la segunda prueba (duenioAdminIngreso)")
        #Caso de prueba (T,T,T) no es posible, admin.autenticarAdmin() y duenio.autenticarDuenio() no pueden ser ambas verdaeras
        self.assertEqual(duenioAdminIngreso(self.request1, self.adminDatos), "ADMIN") #Caso de prueba (T,T,F)
        self.assertEqual(duenioAdminIngreso(self.request1, self.duenioDatos), "DUENIO") #Caso de prueba (T,F,T)
        self.assertEqual(duenioAdminIngreso(self.request1, self.noUser), "INVALIDO") #Caso de pureba (T,F,F)
        #Caso de prueba (F,T,T) no es posible, admin.autenticarAdmin() y duenio.autenticarDuenio() no pueden ser ambas verdaeras
        self.assertEqual(duenioAdminIngreso(self.request2, self.adminDatos), "SEND")  #Caso de pureba (F,T,F)
        self.assertEqual(duenioAdminIngreso(self.request2, self.duenioDatos), "SEND") #Caso de pureba (F,F,T)
        self.assertEqual(duenioAdminIngreso(self.request2, self.noUser), "SEND") #Caso de pureba (F,F,F)

    def tearDown(self):
        print("Destruyendo el contexto")
        del(self.bodega1)
        del(self.bodega2)
        del(self.bodega1Datos)
        del(self.bodega2Datos)
        del(self.request1)
        del(self.request2)
        del(self.duenio)
        del(self.duenioDatos)
        del(self.admin)
        del(self.adminDatos)
        del(self.noUser)