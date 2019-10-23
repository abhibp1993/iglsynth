# Installation Instructions



**Step 1: Get the Docker Image**

Assuming you have installed Docker. 

```bash
$ docker pull abhibp1993/iglsynth:dev
```



**Step 2: Get the HW code**

Download `HW-Code.zip`  from Canvas and unzip it at some location. You should see the following code structure:

```
iglsynth                          <------------- (base)
	- FMR_HW
		- gw_graph.py
		- prod_ts_aut.py
		- ... 
		
	- iglsynth
		- game
		- logic
		- solver 
		- util
		
	- ...
```



**Step 3: Configure PyCharm**

1. In PyCharm **(Professional)**, select the base folder `iglsynth` as project. 

   * You must have PyCharm Professional to use Docker. 

   * To get it, register for student license. 

   * Download PyCharm Professional.

   * Enter your login credentials. 

     

2. Create Docker Server

   * Go to `File -> Settings -> Build, Execution and Deployment -> Docker` 

   * Click on `+` symbol

   * Enter name as `IGLSynth`. 

   * In `Connect to Docker Daemon with`, select TCP socket with default engine API URL.

   * It should show `Connection successful` below path mappings box.  

     

3. Configure Project Interpreter. 

   * Go to `File -> Settings -> Project: iglsynth -> Project Interpreter  ` 

   * Click on the gear symbol, and select `Docker`. 
   * Select `IGLSynth` as Server. 
   * Enter image name as `abhibp1993/iglsynth:dev` 
   * Enter Python Interpreter Path as `python3`

   

That's it. 



## Running the code

There are three ways to run the code. 



1. **[Easiest]** If using PyCharm, just `Run` the file. PyCharm will take care of configurations for you. 

   

2. **[Moderate]** In PyCharm, 

   * Go to `View -> Tool Windows -> Docker` (on Windows) or `View -> Tool Windows -> Services` (on Ubuntu). I don't know about Mac! 

   * Select and Run `IGLSynth` 

   * Find `abhibp1993/iglsynth:dev` in the list of images. Run it. 

   * The above step will create a container. Run it. 

   * Copy name of container. 

   * Go to `View -> Tool Windows -> Terminal` 

     ```bash
     PC$ docker exec -it <container_name> /bin/bash
     Docker$ cd home/iglsynth
     Docker$ python3 -m pytest FMR_HW/<file_name>.py
     ```

     

   

3. If running everything from terminal, then 

   ```bash
   PC$ docker run -it -v <PATH/TO/UNZIPPED/FOLDER>:/home/iglsynth abhibp1993/iglsynth:dev 
   Docker$ cd /home/iglsynth/
   Docker$ python3 -m pytest <file_name>.py
   ```



Check if all tests are pass or not. Ignore any warnings. 

