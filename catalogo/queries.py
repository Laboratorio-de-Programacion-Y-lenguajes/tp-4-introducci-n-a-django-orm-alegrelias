from __future__ import annotations

from django.db.models import Count, F, Q

from .models import Autor, Libro


def libros_por_categoria(nombre_categoria: str):
    return Libro.objects.filter(categorias__nombre=nombre_categoria)


def autores_con_mas_de_n_libros(n: int):
    return Autor.objects.annotate(cantidad_libros=Count("libro", distinct=True)).filter(cantidad_libros__gt=n)


def libros_sin_disponibilidad():
    return Libro.objects.annotate(
            activos=Count("prestamo", filter=Q(prestamo__fecha_devolucion__isnull=True))
        ).filter(activos__gte=F("cantidad_total"))


def top_n_libros_mas_prestados(n: int):
    return Libro.objects.annotate(total_prestamos=Count("prestamo")).order_by("-total_prestamos", "titulo")[:n]
