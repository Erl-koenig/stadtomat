FROM nginx:1.27.2-alpine-slim

COPY ./dist/ /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]