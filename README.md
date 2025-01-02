## ShortenURL

### Setting
> Prepare Environment Variable
```
DJANGO_SUPERUSER_USERNAME=
DJANGO_SUPERUSER_EMAIL=
DJANGO_SUPERUSER_PASSWORD=
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
FACEBOOK_CLIENT_ID=
FACEBOOK_CLIENT_SECRET=
ALLOWED_HOSTS=          # Seperate hosts with comma
```

### Deployment
> Build Image \
`docker build -t <image_name> .`

> Run Container \
> `docker run -d -p 8000:8000 --env-file <env_file_location> <image_name>`

