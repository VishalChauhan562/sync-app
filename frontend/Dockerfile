# Use Node.js 18 (or a later version) official image as a base
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json for installing dependencies
COPY frontend/package.json frontend/package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend files (src, public, etc.)
COPY frontend /app

# Expose the port where the app will run (default Vite port is 5173)
EXPOSE 5173

# Build and start the app using Vite, listening on all network interfaces
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
