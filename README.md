- Create a symlink with name docker-compose.yml to docker-compose.local.yml
```sh
   ln -s docker-compose.yml  docker-compose.local.yml
 ```


- Rename .env_sample to .env and change it settings accordingly for the project

- Inside project root rename local_settings_sample.py to local_settings.py and
 change it settings accordingly for the project

- Bulid docker image
```sh
   docker-compose build
 ```

- Run external services
```sh
   docker-compose -f external_services.yml up -d
 ```

- Run the project in docker
```sh
   docker-compose -f docker-compose.local.yml up -d
 ```