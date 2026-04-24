/* ════════════════════════════════════════════════════════════════
   ExplorAR Glasses — Frontend Logic (app.js)
   All API calls go to Flask backend on http://localhost:5000
   ════════════════════════════════════════════════════════════════ */

const BASE = window.location.origin + "/api";

// ═══ TAB NAVIGATION ════════════════════════════════════════════════════════

document.querySelectorAll(".pill").forEach(btn => {
  btn.addEventListener("click", () => {
    const tab = btn.dataset.tab;
    switchTab(tab);
  });
});

document.querySelectorAll(".dash-card").forEach(card => {
  card.addEventListener("click", () => {
    const tab = card.dataset.tab;
    switchTab(tab);
  });
});

function switchTab(tab) {
  document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));
  document.querySelectorAll(".pill").forEach(b => b.classList.remove("active"));
  document.getElementById("tab-" + tab).classList.add("active");
  document.getElementById("nav-" + tab).classList.add("active");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// ═══ HELPERS ════════════════════════════════════════════════════════════════

function loading(id) {
  document.getElementById(id).innerHTML = `
    <div class="result-loading">
      <div class="spinner"></div> Fetching real-time data…
    </div>`;
}

function showError(id, msg) {
  document.getElementById(id).innerHTML = `<div class="result-error">⚠️ ${msg}</div>`;
}

function disableBtn(id) { const b = document.getElementById(id); if (b) b.disabled = true; }
function enableBtn(id)  { const b = document.getElementById(id); if (b) b.disabled = false; }

async function apiFetch(url, options = {}) {
  const resp = await fetch(url, options);
  const data = await resp.json();
  if (!resp.ok) throw new Error(data.error || "Unknown error from server");
  if (data.error) throw new Error(data.error);
  return data;
}

// ═══ HEALTH CHECK ════════════════════════════════════════════════════════════

async function checkHealth() {
  const badge = document.getElementById("backend-status");
  try {
    const data = await apiFetch(BASE + "/health");
    badge.innerHTML = `<span class="dot ok"></span> Backend running — ${data.modules.length} modules active`;
    badge.style.color = "#3b6e4a";
  } catch {
    badge.innerHTML = `<span class="dot error"></span> Backend offline — start Flask on port 5000`;
    badge.style.color = "#a0303f";
  }
}
checkHealth();

// ═══ CONTEXT ═════════════════════════════════════════════════════════════════

async function fetchContext() {
  const place = document.getElementById("context-input").value.trim();
  if (!place) { showError("context-result", "Please enter a place name."); return; }

  loading("context-result");
  disableBtn("context-btn");
  try {
    const d = await apiFetch(`${BASE}/context?place=${encodeURIComponent(place)}`);
    
    // Create the result container structure
    document.getElementById("context-result").innerHTML = `
      <div class="result-header" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
        <span class="tag" style="background:var(--primary-d)">📡 ${d.category?.toUpperCase() || "LOCATION"}</span>
        <span class="tag" style="background:rgba(255,255,255,0.1)">#${d.engine?.split(' ')[0] || 'AI'}</span>
      </div>
      <div class="section-title" style="font-size:1.6rem; color:var(--text)">${d.place}</div>
      <div id="typing-desc" class="typing-text" style="min-height:60px; line-height:1.6; margin-bottom:20px; color:var(--text-muted)"></div>
      
      <div class="section-title" style="font-size:0.9rem; margin-top:20px; opacity:0.8">NEARBY SCAN HIGHLIGHTS</div>
      <div class="lang-hints" id="interactive-hints"></div>
    `;

    // 1. Typing Animation Effect
    const descEl = document.getElementById("typing-desc");
    let i = 0;
    const speed = 15; 
    function typeWriter() {
      if (i < d.description.length) {
        descEl.innerHTML += d.description.charAt(i);
        i++;
        setTimeout(typeWriter, speed);
      }
    }
    typeWriter();

    // 2. Interactive Highlights
    const hintsEl = document.getElementById("interactive-hints");
    if (d.nearby_highlights?.length) {
      d.nearby_highlights.forEach(n => {
        const span = document.createElement("span");
        span.className = "hint-chip";
        span.style.cursor = "pointer";
        span.innerText = n;
        span.onclick = () => {
          document.getElementById("context-input").value = n;
          fetchContext();
        };
        hintsEl.appendChild(span);
      });
    } else {
      hintsEl.innerHTML = "<em>No additional data points found.</em>";
    }

  } catch (e) { showError("context-result", e.message); }
  finally { enableBtn("context-btn"); }
}

document.getElementById("context-input").addEventListener("keydown", e => {
  if (e.key === "Enter") fetchContext();
});

// ═══ WEATHER ══════════════════════════════════════════════════════════════════

async function fetchWeather() {
  const city = document.getElementById("weather-input").value.trim();
  if (!city) { showError("weather-result", "Please enter a city name."); return; }

  loading("weather-result");
  disableBtn("weather-btn");
  try {
    const d = await apiFetch(`${BASE}/weather?city=${encodeURIComponent(city)}`);
    document.getElementById("weather-result").innerHTML = `
      <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-bottom:8px;">
        <img class="weather-icon" src="${d.icon}" alt="${d.condition}" />
        <div>
          <div class="section-title" style="margin-top:0">${d.city}</div>
          <p style="font-size:2rem;font-weight:700;color:var(--primary-d)">${d.temperature_c}°C</p>
          <p style="color:var(--text-muted)">${d.description}</p>
        </div>
      </div>
      <div class="info-grid">
        <div class="info-card"><div class="label">Feels Like</div><div class="value">${d.feels_like_c}°C</div></div>
        <div class="info-card"><div class="label">Humidity</div><div class="value">${d.humidity_percent}%</div></div>
        <div class="info-card"><div class="label">Wind</div><div class="value">${d.wind_speed_kmh} km/h</div></div>
        <div class="info-card"><div class="label">Visibility</div><div class="value">${d.visibility_km} km</div></div>
      </div>
    `;
  } catch (e) { showError("weather-result", e.message); }
  finally { enableBtn("weather-btn"); }
}

document.getElementById("weather-input").addEventListener("keydown", e => {
  if (e.key === "Enter") fetchWeather();
});

// ═══ NAVIGATION ═══════════════════════════════════════════════════════════════

async function fetchNavigation() {
  const src  = document.getElementById("nav-source").value.trim();
  const dest = document.getElementById("nav-dest").value.trim();
  const mode = document.getElementById("nav-mode").value;
  if (!src || !dest) { showError("navigation-result", "Please fill both source and destination."); return; }

  loading("navigation-result");
  try {
    const d = await apiFetch(
      `${BASE}/navigation?source=${encodeURIComponent(src)}&destination=${encodeURIComponent(dest)}&mode=${mode}`
    );

    if (d.error) { showError("navigation-result", d.error); return; }

    document.getElementById("navigation-result").innerHTML = `
      <div class="info-grid">
        <div class="info-card"><div class="label">From</div><div class="value" style="font-size:0.9rem">${d.source}</div></div>
        <div class="info-card"><div class="label">To</div><div class="value" style="font-size:0.9rem">${d.destination}</div></div>
        <div class="info-card"><div class="label">Distance</div><div class="value">${d.total_distance}</div></div>
        <div class="info-card"><div class="label">Duration</div><div class="value">${d.total_duration}</div></div>
      </div>
      <div class="section-title">Navigation Sync Active</div>
      <p style="color:var(--text-muted); font-size:0.9rem">Route data is being synchronized with your ExplorAR Glasses heads-up display.</p>
    `;
  } catch (e) { showError("navigation-result", e.message); }
}

// ═══ TRANSLATION ══════════════════════════════════════════════════════════════

function setLang(code) {
  document.getElementById("translate-lang").value = code;
}

async function fetchTranslation() {
  const text   = document.getElementById("translate-text").value.trim();
  const target = document.getElementById("translate-lang").value.trim();
  if (!text)   { showError("translation-result", "Please enter text to translate."); return; }
  if (!target) { showError("translation-result", "Please enter a target language code."); return; }

  loading("translation-result");
  try {
    const d = await apiFetch(`${BASE}/translate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, target_language: target })
    });
    document.getElementById("translation-result").innerHTML = `
      <div class="section-title">Translation</div>
      <div class="translated-text">${d.translated_text}</div>
      <div class="info-grid">
        <div class="info-card"><div class="label">Original</div><div class="value" style="font-size:0.9rem">${d.original_text}</div></div>
        <div class="info-card"><div class="label">Source Language</div><div class="value">${d.detected_source_language}</div></div>
        <div class="info-card"><div class="label">Target Language</div><div class="value">${d.target_language}</div></div>
      </div>
    `;
  } catch (e) { showError("translation-result", e.message); }
}

// ═══ OCR ══════════════════════════════════════════════════════════════════════

async function previewAndOCR(event) {
  const file = event.target.files[0];
  if (!file) return;

  // Show preview
  const preview = document.getElementById("ocr-preview");
  preview.src = URL.createObjectURL(file);
  preview.style.display = "block";

  loading("ocr-result");

  const formData = new FormData();
  formData.append("image", file);

  try {
    const resp = await fetch(`${BASE}/ocr`, { method: "POST", body: formData });
    const d = await resp.json();
    if (d.error) { showError("ocr-result", d.error); return; }
    document.getElementById("ocr-result").innerHTML = `
      <div class="section-title">Extracted Text</div>
      <p style="white-space:pre-wrap;font-size:0.95rem">${d.extracted_text || "(No text found)"}</p>
      <div class="info-grid" style="margin-top:14px">
        <div class="info-card"><div class="label">Word Count</div><div class="value">${d.word_count}</div></div>
        <div class="info-card"><div class="label">Engine</div><div class="value" style="font-size:0.85rem">${d.engine}</div></div>
      </div>
    `;
  } catch (e) { showError("ocr-result", e.message); }
}

// ═══ SPEECH RECOGNITION ══════════════════════════════════════════════════════
function startSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    alert("Voice recognition is not supported in this browser. Please use Chrome or Edge.");
    return;
  }

  const recognition = new SpeechRecognition();
  const micBtn = document.getElementById("mic-btn");
  const input = document.getElementById("voice-input");

  recognition.onstart = () => {
    micBtn.innerText = "🛑";
    micBtn.style.color = "red";
    input.placeholder = "Listening...";
  };

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    input.value = transcript;
    fetchVoice(); // Automatically process after speech
  };

  recognition.onerror = () => {
    stop();
  };

  recognition.onend = () => {
    stop();
  };

  function stop() {
    micBtn.innerText = "🎙️";
    micBtn.style.color = "var(--primary)";
    input.placeholder = "e.g. How is the weather in Kota right now?";
  }

  recognition.start();
}

// ═══ VOICE ════════════════════════════════════════════════════════════════════

function setVoice(text) {
  document.getElementById("voice-input").value = text;
}

async function fetchVoice() {
  const query = document.getElementById("voice-input").value.trim();
  if (!query) { showError("voice-result", "Please enter a question."); return; }

  loading("voice-result");
  try {
    const d = await apiFetch(`${BASE}/voice/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query })
    });

    const inner = renderVoiceResponse(d);
    document.getElementById("voice-result").innerHTML = `
      <div class="section-title">Intent: <span style="color:var(--primary-d)">${d.intent}</span></div>
      ${inner}
    `;
  } catch (e) { showError("voice-result", e.message); }
}

function renderVoiceResponse(d) {
  const r = d.response;
  if (!r) return "<p>No response.</p>";
  if (r.error) return `<div class="result-error">⚠️ ${r.error}</div>`;

  if (d.intent === "weather" && r.temperature_c !== undefined) {
    return `
      <div class="info-grid">
        <div class="info-card"><div class="label">City</div><div class="value">${r.city}</div></div>
        <div class="info-card"><div class="label">Temp</div><div class="value">${r.temperature_c}°C</div></div>
        <div class="info-card"><div class="label">Condition</div><div class="value">${r.description}</div></div>
        <div class="info-card"><div class="label">Humidity</div><div class="value">${r.humidity_percent}%</div></div>
      </div>`;
  }
  if (d.intent === "context" && r.description) {
    return `<p>${r.description}</p>`;
  }
  if (d.intent === "navigation" && r.total_distance) {
    return `<p>🗺️ <strong>${r.source}</strong> → <strong>${r.destination}</strong><br>
      Distance: ${r.total_distance} · Duration: ${r.total_duration}</p>`;
  }
  if (r.message) {
    return `<p>${r.message}</p>`;
  }
  return `<pre style="font-size:0.82rem;overflow:auto">${JSON.stringify(r, null, 2)}</pre>`;
}

document.getElementById("voice-input").addEventListener("keydown", e => {
  if (e.key === "Enter") fetchVoice();
});
