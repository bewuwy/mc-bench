import os
import shutil
import subprocess

server_folder = "server"
resources_folder = "resources"

# clean up old server folder
if os.path.exists(server_folder):
    shutil.rmtree(server_folder)

os.makedirs(server_folder, exist_ok=True)

# copy resources folder to server folder
shutil.copytree(resources_folder, server_folder, dirs_exist_ok=True)

# run the server
process = subprocess.Popen(
    ["java", "-jar", "paper.jar"],
    cwd=server_folder,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=0,
    env={**os.environ, "PYTHONUNBUFFERED": "1"}
)


while True:
    output = process.stdout.readline()
    if output == '' and process.poll() is not None:
        break
    if output:
        print(output.rstrip(), flush=True)  # Force flush
        
        if "Done (" in output.rstrip():
            print("Server is ready.", flush=True)
            break

process.stdin.write("stop\n")
process.stdin.flush()

while True:
    output = process.stdout.readline()
    if output == '' and process.poll() is not None:
        break
    if output:
        print(output.rstrip(), flush=True)

process.wait()
