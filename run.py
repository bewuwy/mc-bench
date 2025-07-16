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
    bufsize=1
)

for line in iter(process.stdout.readline, ''):
    print(line.rstrip())

    if "Done (" in line.rstrip():
        print("Server is ready.")
        break

process.stdin.write("stop\n")
process.stdin.flush()

for line in iter(process.stdout.readline, ''):
    print(line.rstrip())

process.wait()
