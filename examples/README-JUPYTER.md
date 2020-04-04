# Instructions for Jupyter Notebooks

On Ubuntu:
```bash
docker run -p 8888:8888 --rm -v $(pwd):/opt/notebook iglsynth-test /bin/bash -c "jupyter notebook
 --ip=0.0.0.0 --notebook-dir=/opt/notebook --allow-root --no-browser"
 ```

Can be adopted to Windows by changing `$(pwd)` appropriately.