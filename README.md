### Install  
```bash
# postgres build 
git clone git@github.com:docker-library/postgres.git
docker build -t jhsong/postgres postgres/10/

# or pull from repository
docker pull jhsong/postgres 

docker run -p54320:5432 --name drugcentral -e POSTGRES_PASSWORD='docker' -d jhsong/postgres

echo 'create database drugcentral' | docker exec -i drugcentral psql -Upostgres

# You can download drugcentral.dump.08292017.sql.gz from http://drugcentral.org/download . 
gzip -d -c drugcentral.dump.08292017.sql.gz | docker exec -i drugcentral psql -Upostgres drugcentral
```
