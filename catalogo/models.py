from __future__ import annotations

from django.db import models
from django.utils import timezone


class Autor(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    bibliografia = models.TextField(blank=True)

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True)
    fecha_publicacion = models.DateField()
    cantidad_total = models.PositiveIntegerField(default=0)
    autor = models.ForeignKey(Autor, on_delete=models.PROTECT)
    categorias = models.ManyToManyField(Categoria)
    
    def __str__(self):
        return self.titulo

    def prestamos_activos(self) -> int:
        return self.prestamo.filter(fecha_devolucion__isnull=True).count()

    def disponibles(self) -> int:
        return max(0, self.cantidad_total - self.prestamos_activos())

    def tiene_disponibles(self) -> bool:
        return self.disponibles() >= 1


class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.PROTECT, related_name='prestamo')
    nombre_prestatario = models.CharField(max_length=200)
    fecha_prestamo = models.DateField(default=timezone.now)
    fecha_devolucion = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"
        ordering = ['-fecha_prestamo']

    def __str__(self):
        return f"{self.libro.titulo} -> Prestado a {self.nombre_prestatario}"