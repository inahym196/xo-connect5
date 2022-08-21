FROM node:18 AS builder
WORKDIR /build
COPY package*.json ./
#RUN npm ci --only=production
RUN npm ci 

FROM gcr.io/distroless/nodejs:18-debug
WORKDIR /usr/app
ENV NODE_ENV development
COPY --from=builder --chown=nonroot:nonroot /build/package.json ./package.json
COPY --from=builder --chown=nonroot:nonroot /build/node_modules ./node_modules
USER nonroot
EXPOSE 80
CMD [ "./src/server.js" ]
#ENTRYPOINT [ "sh" ]