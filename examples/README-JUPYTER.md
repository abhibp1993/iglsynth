# Instructions for Running Jupyter Notebooks

Two steps

1. Create docker container 

    On Ubuntu:
    ```bash
    docker run -p 8888:8888 --rm -v $(pwd):/home/iglsynth iglsynth-test /bin/bash -c "jupyter notebook
     --ip=0.0.0.0 --notebook-dir=/home/iglsynth --allow-root --no-browser"
     ```
    
    Can be adopted to Windows by changing `$(pwd)` appropriately.
    
2. Click on the hyperlink to launch the Jupyter notebook in the browser. 
