from django.conf import settings
import oracledb
import logging

logger = logging.getLogger(__name__)

def get_user_data(cedula: str, fecha_expedicion: str):
    """
    Se conecta a la base de datos de Oracle, ejecuta el procedimiento almacenado SP_VALIDAID
    y devuelve los datos del usuario.

    Si el procedimiento no devuelve filas, esta función devuelve None, lo que indica
    que el asociado no fue encontrado.

    Args:
        cedula (str): El número de cédula del usuario.
        fecha_expedicion (str): La fecha de expedición en formato 'AAAA/MM/DD'.

    Returns:
        dict: Un diccionario con los datos del usuario si se encuentra.
        None: Si el usuario no se encuentra o si ocurre un error.
    """
    print("Conectando a Oracle con cédula:", cedula, "y fecha de expedición:", fecha_expedicion)
    try:
        db = settings.DATABASES['oracle']
        dsn = f"{db['HOST']}:{db['PORT']}/{db['NAME']}"
        
        with oracledb.connect(user=db['USER'], password=db['PASSWORD'], dsn=dsn) as connection:
            with connection.cursor() as cursor:
                cursor_out = cursor.var(oracledb.CURSOR)
                cursor.callproc('SP_VALIDAIDE', [cedula, fecha_expedicion, cursor_out])
                result_cursor = cursor_out.getvalue()

                if result_cursor:
                    row = result_cursor.fetchone()
                    if row:
                        cols = [col[0].lower() for col in result_cursor.description]
                        user_data = dict(zip(cols, row))
                        return user_data
        
        return None

    except oracledb.DatabaseError as e:
        logger.error(f"Error de base de datos Oracle en SP_VALIDAIDE: {e}", exc_info=True)
        return None
    except Exception as e:
        logger.error(f"Error inesperado en oracle_service: {e}", exc_info=True)
        return None
