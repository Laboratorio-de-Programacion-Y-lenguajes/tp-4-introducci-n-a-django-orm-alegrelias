import models

from __future__ import annotations

from django.db.models import Count, Q

from .models import Autor, Libro


def libros_por_categoria(nombre_categoria: str):
    return Libro.objects.filter(categorias__nombre=nombre_categoria)


def autores_con_mas_de_n_libros(n: int):
    return Autor.objects.annotate(cantidad_libros=Count("libro", distinct=True)).filter(cantidad_libros__gt=n)


def libros_sin_disponibilidad():
    return Libro.objects.annotate(
            activos=Count("prestamo", filter=Q(prestamo__fecha_devolucion__isnull=True))
        ).filter(activos__gte=models.F("cantidad_total"))


def top_n_libros_mas_prestados(n: int):
    """
    Devuelve los N libros con más préstamos (en total, sin importar si están activos).

    Args:
        n: cantidad de libros a retornar

    Returns:
        QuerySet[Libro] con hasta n elementos, ordenados de más a menos prestados.

    Pista:
        Libro.objects.annotate(total_prestamos=Count("prestamo"))
                    .order_by("-total_prestamos")[:n]
    """
    # TODO: implementar con annotate + order_by + slicing
    raise NotImplementedError
