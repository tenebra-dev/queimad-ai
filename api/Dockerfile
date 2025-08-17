# Build stage
FROM node:18-alpine AS builder

# Install pnpm
RUN npm install -g pnpm

WORKDIR /app

# Copy package files
COPY package*.json pnpm-lock.yaml* ./

# Install dependencies
RUN pnpm install --frozen-lockfile --prod

# Copy source code
COPY . .

# Build the application
RUN pnpm build

# Production stage
FROM node:18-alpine

WORKDIR /app

# Create uploads directory
RUN mkdir -p uploads

# Copy built application
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001

# Change ownership
RUN chown -R nodejs:nodejs /app
USER nodejs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/api/health', (res) => process.exit(res.statusCode === 200 ? 0 : 1))"

# Start the application
CMD ["node", "dist/index.js"]
