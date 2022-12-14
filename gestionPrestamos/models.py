from django.db import models

# Create your models here.

class Libro(models.Model):
    Isbn=models.CharField(max_length=25,primary_key=True)    # Defino una longitud y le asigno la llave primaria 
    titulo=models.TextField(max_length=100,unique=True,null=False) # Defino una longitud, digo q debe ser unico en la base de datos y que no puede estar vacio
    editorial=models.CharField(max_length=50,null=False)
    autor=models.CharField(max_length=50,null=False)
    no_page=models.IntegerField(null=True)
    
    def __str__(self):
        return self.titulo
    
class Estudiante(models.Model):
    documento=models.IntegerField(primary_key=True)
    nombre=models.TextField(max_length=50,null=False)
    apellido=models.TextField(max_length=50,null=False)
    email=models.EmailField(unique=True)
    telefono=models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre+" "+self.apellido
    
class Prestamo(models.Model):
    id=models.AutoField(primary_key=True)    # Crea un Id automaticamente y es la llave primaria 
    estudiante=models.ForeignKey(Estudiante, on_delete=models.CASCADE) # Creo la llave foranea con la clase predecesora 
    libro=models.ForeignKey(Libro, on_delete=models.CASCADE) # Con .CASCADE deja eliminar el dato junto con todas sus relaciones
    fecha=models.DateField(auto_now=True)

class Devolucion(models.Model):
    id=models.AutoField(primary_key=True)
    prestamo=models.OneToOneField(Prestamo, on_delete=models.CASCADE)
    fecha=models.DateField(auto_now=True)