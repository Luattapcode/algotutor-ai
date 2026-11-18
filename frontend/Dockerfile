# Use official Node runtime
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy frontend source code
COPY . .

# Build Next.js for production
RUN npm run build

# Expose port 3000
EXPOSE 3000

# Start Next.js production server
CMD ["npm", "run", "start"]