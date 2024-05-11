class UsuariosRouter:

    def db_for_read(self, model, **hints):
        """
        Las lecturas van a la réplica.
        """
        if model._meta.verbose_name == 'usuarios':
            return 'usuarios'
        else:
            return 'default'

    def db_for_write(self, model, **hints):
        """
        Las escrituras van a la base de datos principal.
        """
        if model._meta.verbose_name == 'usuarios':
            return 'usuarios'
        else:
            return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Permite relaciones si los modelos están en la misma base de datos.
        """
        db_obj1 = hints.get('instance', obj1)._state.db
        db_obj2 = hints.get('instance', obj2)._state.db
        return db_obj1 == db_obj2

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Todas las migraciones van a la base de datos principal.
        """
        return db == 'default'