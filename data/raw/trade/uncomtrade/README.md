# UN Comtrade Dataset

This directory stores raw and processed trade datasets used by Geoflation.

## Source

United Nations Comtrade Database

https://comtradeplus.un.org/

## Scope

Dataset Version:
Latest available year

Countries:
G20 economies

Commodities:
All available HS commodity categories

Flow:
Exports

Purpose

This dataset is used to build the weighted directed trade network powering:

- Trade shock propagation
- Country vulnerability scoring
- Graph analytics
- Future Graph Neural Networks

Directory Structure

raw/
Original downloaded files

processed/
Cleaned datasets

metadata/
Country mappings and auxiliary lookup tables
