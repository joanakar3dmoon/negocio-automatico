# negocio-automatico

## Weather dashboard

The `dashboard/` folder contains a responsive weather dashboard powered by the public [Open-Meteo](https://open-meteo.com/) weather and air-quality APIs. It requires no API key.

### Run locally

From the repository root:

```bash
cd dashboard
python -m http.server 8080
```

Open http://localhost:8080. The dashboard supports city search, browser geolocation, Celsius/Fahrenheit units, current conditions, air quality, metrics, and a seven-day forecast.

### Deploy with Render

The root `render.yaml` now defines both the existing API and a static dashboard service. Create a new Blueprint in Render and select this repository. The dashboard will be published as `negocio-automatico-dashboard.onrender.com` (or the URL assigned by Render).

Weather data is fetched directly in the browser from Open-Meteo, so no environment variable or API key is required.
