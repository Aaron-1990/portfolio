# Frontend Dockerfile

FROM node:18-alpine

# Establecer directorio de trabajo
WORKDIR /app

# Copiar package files
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar código de la aplicación
COPY . .

# Exponer puerto
EXPOSE 5173

# Comando por default (development)
CMD ["npm", "run", "dev", "--", "--host"]
