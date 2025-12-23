#!/bin/bash
# Nuke everything local for a fresh start

echo "Stopping containers..."
cd local
docker compose down -v --remove-orphans

echo "Cleaning data directories..."
cd ..
rm -rf data/landing/*
rm -rf data/clean/*

echo "Pruning Docker volumes (optional, force with -f if needed)..."
# docker volume prune -f 

echo "Cleanup complete. Run 'cd local && docker compose up -d' to restart."
