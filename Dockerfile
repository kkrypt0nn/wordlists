FROM alpine:latest
# FROM ubuntu:latest

COPY wordlists /wordlists

WORKDIR /wordlists