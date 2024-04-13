from ..models import Solicitud

def get_solicitudes():
    solicitudes = Solicitud.objects.all()
    return solicitudes

def get_solicitud(sol_pk):
    solicitud = Solicitud.objects.get(pk=sol_pk)
    return solicitud

def create_solicitud(sol):
    sol.save()
    return sol

def update_solicitud(sol_pk, new_sol):
    solicitud = get_solicitud(sol_pk)
    solicitud.fecha_solicitud = new_sol.fecha_solicitud
    solicitud.anio_solicitud = new_sol.anio_solicitud
    solicitud.estado = new_sol.estado
    solicitud.save()
    return solicitud

def delete_solicitud(sol_pk):
    solicitud = get_solicitud(sol_pk)
    solicitud.delete()
    return None
