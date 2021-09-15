# Setup

You can use docker for quick prototyping.

Create your `docker-compose.yml` file using `docker-compose.yml.example`
as a base and customize it according to your needs.

```bash
cp docker-compose.yml.example docker-compose.yml
```

## Start the infrastructure

```bash
docker-compose up
```

## Update the infrastructure components

### Turn off the infrastructure

```bash
docker-compose stop
```

### Update the desired components

According what you want to update following a new release, you can just
update your single containers.

For example, given the `docker-compose.yml.example` file, if you want to
update only a single container (`web` in this case) you can use:

```bash
docker-compose build --no-cache web
```

### Start the infrastructure again

```bash
docker-compose up
```
