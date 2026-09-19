const state = { unit: 'celsius', location: { name: 'Lisbon', country: 'Portugal', latitude: 38.7223, longitude: -9.1393 }, forecast: null };
const $ = (id) => document.getElementById(id);
const icons = { clear: '☀', partly: '◒', cloudy: '☁', rain: '☂', snow: '❄', storm: 'ϟ', fog: '≋' };
const descriptions = { 0:['Clear sky','clear'], 1:['Mainly clear','partly'], 2:['Partly cloudy','partly'], 3:['Overcast','cloudy'], 45:['Foggy','fog'], 48:['Rime fog','fog'], 51:['Light drizzle','rain'], 53:['Drizzle','rain'], 55:['Dense drizzle','rain'], 61:['Light rain','rain'], 63:['Rain','rain'], 65:['Heavy rain','rain'], 71:['Light snow','snow'], 73:['Snow','snow'], 75:['Heavy snow','snow'], 80:['Rain showers','rain'], 81:['Rain showers','rain'], 82:['Heavy showers','rain'], 95:['Thunderstorm','storm'], 96:['Thunderstorm','storm'], 99:['Thunderstorm','storm'] };
function weather(code) { const item = descriptions[code] || ['Variable conditions','partly']; return { name:item[0], icon:icons[item[1]] }; }
function temp(value) { return Math.round(state.unit === 'celsius' ? value : value * 9 / 5 + 32); }
function degree(value) { return `${temp(value)}°`; }
function formatDate(date, options) { return new Intl.DateTimeFormat(undefined, options).format(date); }
function setStatus(message = '') { $('status').textContent = message; }
function formatTime(value) { return value ? formatDate(new Date(value), { hour:'numeric', minute:'2-digit' }) : '—'; }
function compass(degrees) { return ['N','NE','E','SE','S','SW','W','NW'][Math.round(degrees / 45) % 8]; }
function render(data) {
  const current = data.current, daily = data.daily;
  const condition = weather(current.weather_code);
  $('current-city').textContent = `${state.location.name}, ${state.location.country_code || state.location.country.slice(0,2).toUpperCase()}`;
  $('current-date').textContent = formatDate(new Date(current.time), { weekday:'long', month:'long', day:'numeric' });
  $('updated-at').textContent = `Updated ${formatTime(current.time)}`;
  $('current-temp').textContent = temp(current.temperature_2m);
  $('current-condition').textContent = condition.name;
  $('current-icon').textContent = condition.icon;
  $('feels-like').textContent = temp(current.apparent_temperature);
  $('humidity').textContent = `${Math.round(current.relative_humidity_2m)}%`;
  $('wind').textContent = `${Math.round(current.wind_speed_10m)} km/h`;
  $('wind-direction').textContent = `${compass(current.wind_direction_10m)} · ${Math.round(current.wind_direction_10m)}°`;
  $('precipitation').textContent = `${Number(current.precipitation || 0).toFixed(1)} mm`;
  const uv = daily.uv_index_max[0] || 0;
  $('uv-index').textContent = uv.toFixed(1);
  $('uv-label').textContent = uv < 3 ? 'Low exposure' : uv < 6 ? 'Moderate exposure' : 'High exposure';
  $('sunrise').textContent = formatTime(daily.sunrise[0]); $('sunset').textContent = formatTime(daily.sunset[0]);
  $('air-score').textContent = data.airScore ?? '—'; $('air-label').textContent = data.airLabel || 'Air quality unavailable';
  $('forecast-list').innerHTML = daily.time.map((date, index) => { const item = weather(daily.weather_code[index]); const day = new Date(`${date}T12:00:00`); return `<article class="forecast-day ${index === 0 ? 'today' : ''}"><strong>${index === 0 ? 'Today' : formatDate(day,{weekday:'short'})}</strong><span class="day-icon">${item.icon}</span><span class="range">${degree(daily.temperature_2m_max[index])} <span class="low">${degree(daily.temperature_2m_min[index])}</span></span><small>${item.name}</small></article>`; }).join('');
}
async function fetchWeather(location = state.location) {
  setStatus('Fetching the latest conditions…');
  try {
    const params = new URLSearchParams({ latitude:location.latitude, longitude:location.longitude, current:'temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,weather_code,wind_speed_10m,wind_direction_10m', hourly:'pm2_5', daily:'weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max', timezone:'auto', forecast_days:'7' });
    const airParams = new URLSearchParams({ latitude:location.latitude, longitude:location.longitude, current:'pm2_5', timezone:'auto' });
    const [weatherResponse, airResponse] = await Promise.all([fetch(`https://api.open-meteo.com/v1/forecast?${params}`), fetch(`https://air-quality-api.open-meteo.com/v1/air-quality?${airParams}`)]);
    if (!weatherResponse.ok) throw new Error('Weather service unavailable');
    const data = await weatherResponse.json(); const air = airResponse.ok ? await airResponse.json() : null;
    const pm = air?.current?.pm2_5; const score = pm == null ? null : Math.max(0, Math.round(100 - pm * 2.5));
    state.location = location; state.forecast = { ...data, airScore:score, airLabel: pm == null ? null : pm < 12 ? 'Good air quality' : pm < 35 ? 'Fair air quality' : 'Needs attention' }; render(state.forecast); setStatus('');
  } catch (error) { setStatus(`Could not load weather. ${error.message}`); }
}
async function searchCity(event) { event.preventDefault(); const query = $('city-search').value.trim(); if (!query) return; setStatus('Finding that location…'); try { const response = await fetch(`https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(query)}&count=1&language=en&format=json`); const result = await response.json(); if (!result.results?.length) throw new Error('City not found.'); const place = result.results[0]; await fetchWeather({ name:place.name, country:place.country, country_code:place.country_code, latitude:place.latitude, longitude:place.longitude }); $('city-search').value = ''; } catch (error) { setStatus(error.message); } }
function useLocation() { if (!navigator.geolocation) return setStatus('Geolocation is not supported by this browser.'); setStatus('Requesting your location…'); navigator.geolocation.getCurrentPosition(async ({coords}) => { await fetchWeather({ name:'Your location', country:'', country_code:'', latitude:coords.latitude, longitude:coords.longitude }); }, () => setStatus('Location permission was not granted.')); }
$('search-form').addEventListener('submit', searchCity); $('location-button').addEventListener('click', useLocation);
document.querySelectorAll('.unit').forEach(button => button.addEventListener('click', () => { state.unit = button.dataset.unit; document.querySelectorAll('.unit').forEach(item => item.classList.toggle('active', item === button)); if (state.forecast) render(state.forecast); }));
fetchWeather();
