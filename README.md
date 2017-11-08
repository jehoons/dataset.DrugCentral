### Install  

```bash
# postgres build 
git clone git@github.com:docker-library/postgres.git
docker build -t jhsong/postgres postgres/10/

# or pull from repository
docker pull jhsong/postgres 

docker run -p54320:5432 --name drugcentral -e POSTGRES_PASSWORD='docker' -d jhsong/postgres

echo 'create database drugcentral' | docker exec -i drugcentral psql -Upostgres

wget http://192.168.0.97/share/StandigmDB/datasets/drug_central/2017-10/drugcentral.dump.08292017.sql.gz

gzip -d drugcentral.dump.08292017.sql.gz && cat drugcentral.dump.08292017.sql | docker exec -i drugcentral psql -Upostgres drugcentral
```
