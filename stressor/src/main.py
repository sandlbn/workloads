
import uvicorn
import subprocess
from fastapi import FastAPI
    
app = FastAPI()

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)

@app.get('/')
async def index():
    return "Go the /docs route for Swagger UI"

################################################# The end-points/routes for starting stressors ###################################################### 

@app.post('/memory/start')
async def memory_start(utilization: int, duration: int):
    global memory_stressor 
    memory_stressor = subprocess.Popen(["stress-ng", "--vm", "1", "--vm-bytes", str(utilization) + "%", "-t", str(duration) + "m"])
    memory_stressor.wait()
    return "Started virtual memory stressor that uses " + str(utilization) + " percent of the available memory for " + str(duration) + " minutes."

@app.post('/cpu/start')
async def cpu_start(utilization: int, duration: int):
    global cpu_stressor 
    cpu_stressor = subprocess.Popen(["stress-ng", "--cpu", "0", "--cpu-method", "all", "--cpu-load", str(utilization), "-t", str(duration) + "m"])
    cpu_stressor.wait()
    return "Started cpu stressors to utilize all configured CPUs at " + str(utilization) + " percent load for " + str(duration) + " minutes."

@app.post('/hdd/start')
async def hdd_start(workers: int):
    global hdd_stressor 
    hdd_stressor = subprocess.Popen(["stress-ng", "--hdd", str(workers) + ""])
    hdd_stressor.wait()
    return "Started " + str(workers) + " number of HDD stressors to write, read, remove temporary files to test sequential writes and reads"

@app.post('/network/start')
async def network_start(utilization: int, duration: int):
    global network_stressor 
    network_stressor = subprocess.Popen(["stress-ng", "--iomix", "1", "--iomix-bytes", str(utilization) + "%", "-t", str(duration) + "m"])
    network_stressor.wait()
    return "Started a mixed I/O stressor using " + str(utilization) + " percent of the available file system space for " + str(duration) + " minutes."

##################################################### The end-points/routes for stopping stressors ####################################################

@app.post('/memory/stop')
async def memory_stop():
    memory_stressor.terminate()
    memory_stressor.wait()
    return "Stopped all memory stressors"

@app.post('/cpu/stop')
async def cpu_stop():
    cpu_stressor.terminate()
    cpu_stressor.wait()
    return "Stopped all cpu stressors"

@app.post('/hdd/stop')
async def hdd_stop():
    hdd_stressor.terminate()
    hdd_stressor.wait()
    return "Stopped all HDD stressors"

@app.post('/network/stop')
async def network_stop():
    network_stressor.terminate()
    network_stressor.wait()
    return "Stopped all network stressors"