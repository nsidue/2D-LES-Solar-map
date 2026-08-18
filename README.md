# 2D LES Solar Potential Map

A geospatial analysis and data pipeline project designed to estimate building solar potential across NYC's Lower East Side (LES) by combining NYC PLUTO tax lot data, spatial building footprints, and solar irradiance weather metrics.

2026 Contributors: Nabila Siddique

---

## Getting Started

Follow these steps to set up your local development environment using git and mise.

### Prerequisites

Ensure you have the following installed on your machine:

* **Git & Git LFS** (required to pull the 435 MB PLUTO dataset) 
(https://www.theodinproject.com/lessons/foundations-git-basics)
* **mise** (task runner & tool version manager) 
(https://mise.jdx.dev/installing-mise.html)

### Quickstart Setup

1. **Clone the Repository:** Retrieves repository files.
```bash
git clone <repository-url>
cd 2D-LES-Solar-map

```


2. **Fetch Large File Assets:** Downloads 435 MB pluto_26v1.csv. Git does not backup these big files by default.

```bash
git lfs install
git lfs pull

```


3. **Initialize Environment:** Provisions Python 3.11, creates virtual environment, and installs packages.
Run the `mise` setup task to automatically provision Python and all project dependencies:

```bash
mise run setup

```


4. **Launch the Environment:** Opens JupyterLab in your web browser.
Start your working session:

```bash
mise run start

```


---

## Core Tools

| Tool | Description |
| --- | --- |
| **NumPy** | High-performance Python library for numerical computing. Handles multi-dimensional arrays and fast vector/matrix mathematical calculations. |
| **pandas** | Data analysis library providing fast, flexible data structures (`DataFrame`) designed to manipulate, clean, join, and aggregate tabular datasets (e.g., CSVs). |
| **Geopandas** | Geospatial data analysis library making working with easier. It extends the datatypes used by pandas to allow spatial operations on geometric types. Geometric operations are performed by **shapely**. |
| **Shapely** | an extension library of Geopandas which is used to create, manipulate, and analyze planar geometric objects. It relies on files that contain coordinates and geometries of buildings and can be used on creating maps. Mostly used for creating plygons, points and lines |
| **Folium** | Python library that allows you to create an interactive map and goes hand-in-hand with Geopandas to filter out **geojson**/csv files to create objects on a map. 
| **GeoJSON Files** | Just a JSON file but used for geospatial data analysis and visualization. |
| **JupyterLab** | Interactive web-based development environment that combines executable code cells, visualization outputs (maps, plots), and rich text documentation. |
| **Matplotlib** | Visualization library for creating static, animated, and interactive publication-quality charts and spatial plots in Python. |
| **Weather API** | An **API (Application Programming Interface)** acts as a digital messenger between your script and an external server. The weather API (Open-Meteo) allows your script to request historical solar irradiance data for specific coordinates. |


<<<<<<< Updated upstream
=======

### Not needed but some third-party tools that were used during the process

- **geojson.io:** Can create custom geojson files without manually using Shapely in the python script.
- **https://www.geeksforgeeks.org/python/visualizing-geospatial-data-using-folium-in-python/:** Tutorial on basics of Folium Library.
- **https://www.lefixea.com/article/solar-power-generation-calculator6:** The formula fo rfinding Solar Panel Capacity of every building and the Solar Power Generation.
- **https://open-meteo.com/en/features#available_apis**  Use this to create your own weather API to expand on more variables than just the Irradiance data we get from the 'fetch_irradianceAPI.py' inside of this repository. 

>>>>>>> Stashed changes
---

**P.S.** - you can look at .mise.toml for more handy task commands and to understand the build recipe.
