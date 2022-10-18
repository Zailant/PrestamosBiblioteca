#from django.shortcuts import render
import json
from django.views import View # Indica al programa q la clase creada se comportara como controlador
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from gestionPrestamos.models import Devolucion, Estudiante, Libro, Prestamo
from django.http import JsonResponse

# Create your views here.

class LibroView(View):
    
    @method_decorator(csrf_exempt)   # Se utiliza para traer los datos desde una url
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    '''def get(self, request):
        Libros=list(Libro.objects.values())  # Busca todos los libros y los da como una lista
        if len(Libros)>0:
            datos={"mensaje": Libros}
        else:
            datos={"mensaje": "No se encontraron Libros"}
        return JsonResponse(datos)'''
    
    '''def get(self, request, isbn):
        libro=list(Libro.objects.filter(Isbn=isbn).values()) # busca un libro en especifico y lo da como resultado
        if len(libro)>0:
            datos={"Libro": libro}
        else:
            datos={"mensaje": "No se encontro el libro."}
        return JsonResponse(datos)'''
    
    def get(self, request, isbn=""):  # Con este codigo buscamos un libro en especifico o nos arroja todos los resultados.
        if len(isbn)>0:
            libro=list(Libro.objects.filter(Isbn=isbn).values())
            if len(libro)>0:
                datos={"Libro": libro}
            else:
                datos={"mensaje": "No se encontro el libro."}
        else: 
            Libros=list(Libro.objects.values())
            if len(Libros)>0:
                datos={"mensaje": Libros}
            else:
                datos={"mensaje": "No se encontraron Libros"}
        return JsonResponse(datos)
    
    def post(self, request): # Para crear elementos desde un api Rest se crea un metodo POST
        data=json.loads(request.body)
        libro=Libro(Isbn=data['Isbn'], titulo=data['titulo'], editorial=data['editorial'], autor=data['autor'], no_page=data['no_page'])
        libro.save()
        datos={'mensaje': 'Libro registrado exitosamente'}
        return JsonResponse(datos)
    
    def put(self,request,isbn):
        data=json.loads(request.body)
        libro=list(Libro.objects.filter(Isbn=isbn).values())
        if len(libro)>0:
            lib=Libro.objects.get(Isbn=isbn)
            lib.titulo=data["titulo"]
            lib.editorial=data["editorial"]
            lib.autor=data["autor"]
            lib.no_page=data["no_page"]
            lib.save()
            mensaje={"mensaje":"Libro Actualizado exitosamente."}
        else:
            mensaje={"mensaje":"No se encontro el Libro."}        
        return JsonResponse(mensaje)
    
    def delete(self,request,isbn):
        libro=list(Libro.objects.filter(Isbn=isbn).values())
        if len(libro)>0:
            Libro.objects.filter(Isbn=isbn).delete()
            mensaje={"mensaje":"Libro Eliminado exitosamente."}
        else:
            mensaje={"mensaje":"No se encontro el Libro."}        
        return JsonResponse(mensaje)
    
# Tabla Prestamos

class PrestamoView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self,request):
        data=json.loads(request.body)        
        try:
            lib=Libro.objects.get(Isbn=data["libro"])
            est=Estudiante.objects.get(documento=data["documento"])
            pres=Prestamo.objects.create(estudiante=est,libro=lib)
            pres.save()
            mensaje={"Mensaje":"Prestamo Registrado."}            
        except Libro.DoesNotExist:
            mensaje={"Mensaje":"El Libro No Existe."}
        except Estudiante.DoesNotExist:
            mensaje={"Mensaje":"El Estudiante No Existe."}
        return JsonResponse(mensaje)
    
class DevolucionView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        data=json.loads(request.body)
        try:
            pres=Prestamo.objects.get(id=data["prestamo"])
            dev=Devolucion.objects.create(prestamo=pres)
            dev.save()
            mensaje={"Mensaje":"Devolucion Registrada."}
        except Prestamo.DoesNotExist:
            mensaje={"Mensaje":"El Prestamo no Existe."}
        except: 
            mensaje={"Mensaje":"Ya Existe Una Devolucion Para Este Prestamo."}
        return JsonResponse(mensaje)