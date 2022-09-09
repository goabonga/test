# environment.py
import os
import subprocess
import time


# This will hold the last response
class APIContext:
    def __init__(self):
        self.response = None
        self.headers = {}
        self.base_url = ""


uvicorn_process = None


def before_all(context):
    """Hook to start FastAPI server before all scenarios."""
    global uvicorn_process

    # Démarre le serveur Uvicorn dans un processus séparé
    uvicorn_process = subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid,  # Pour qu'il fonctionne correctement sur Unix/Linux
    )

    # On attend un peu pour que le serveur soit prêt
    time.sleep(2)


def after_all(context):
    """Hook to stop FastAPI server after all scenarios."""
    global uvicorn_process

    if uvicorn_process:
        # Arrête le serveur Uvicorn
        uvicorn_process.terminate()
        uvicorn_process.wait()


# Initialize the context for the API
def before_scenario(context, scenario):
    # x = 1 / 0  # CAUSE: ZeroDivisionError
    context.api = APIContext()


# import subprocess
# import time
#
# def wait_for_postgres():
#     """Vérifie si PostgreSQL est prêt."""
#     while True:
#         result = subprocess.run(['docker', 'exec', 'flottille-postgres-1', 'pg_isready', '-U', 'username'],
#                                 capture_output=True, text=True)
#         if result.returncode == 0:
#             print("Postgres is ready!")
#             break
#         else:
#             print("Waiting for Postgres to be ready...")
#             time.sleep(2)
#
# def before_all(context):
#     """Lance les services Docker avant tous les tests."""
#     print("Starting Docker services...")
#     result = subprocess.run(['docker', 'compose', 'up', '-d'], capture_output=True, text=True)
#
#     if result.returncode != 0:
#         print(f"Failed to start Docker services: {result.stderr}")
#         raise Exception("Docker services could not be started.")
#     else:
#         print(f"Docker services started successfully: {result.stdout}")
#
#     # Attendre que Postgres soit prêt (ou un autre service essentiel)
#     wait_for_postgres()
#
#
# def after_all(context):
#     """Hook executed after all tests are finished."""
#     print("Stopping Docker services...")
#     result = subprocess.run(['docker', 'compose', 'down', '--volume'], capture_output=True, text=True)
#
#     if result.returncode != 0:
#         print(f"Failed to stop Docker services: {result.stderr}")
#     else:
#         print(f"Docker services stopped successfully: {result.stdout}")
