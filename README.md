### Install  

```
git clone git@github.com:docker-library/postgres.git
docker build -t postgres postgres/10/
docker run -p54320:5432 --name postgres -e POSTGRES_PASSWORD='docker' -d postgres
wget http://192.168.0.97/share/StandigmDB/datasets/drug_central/2017-10/drugcentral.dump.08292017.sql.gz
gzip -d drugcentral.dump.08292017.sql.gz
echo 'create database drugcentral' | docker exec -i postgres psql -Upostgres
cat drugcentral.dump.08292017.sql | docker exec -i postgres psql -Upostgres drugcentral
```
