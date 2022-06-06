# jwtservice
JWT generator for Kong API gateway with an expired date of 180 days

1. Clone this folder to your local machine<br/>
```codeblock
git clone https://github.com/korn-git/jwtservice
```
2. Change your directory to emailservice folder<br/>
```
cd <path>/<to>/jwtservice
```
3. Build your docker image locally<br/>
```
docker build -t <your-docker-image-name> .
```
4. Run you docker container<br/>
```
docker run -d -p <host-port>:5555 --name <your-container-name> jwtservice
```
