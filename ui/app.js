"use strict";
const elem = (id) => document.getElementById(id);
const api = elem("api");
const trip = elem("trip");
const run = elem("run");
const canvas = elem("map");
let endpoint = "";
let active = null;

function status(message, error = false) {
  elem("status").textContent = message;
  elem("status").classList.toggle("error", error);
}

async function request(path, options = {}) {
  const result = await fetch(endpoint + path, {
    signal: AbortSignal.timeout(180000),
    ...options,
  });
  if (!result.ok) {
    const body = await result.json().catch(() => ({}));
    throw new Error(
      typeof body.detail === "string" ? body.detail : "HTTP " + result.status,
    );
  }
  return result.json();
}

async function connect(event) {
  event?.preventDefault();
  const button = elem("connection").querySelector("button");
  button.disabled = run.disabled = trip.disabled = true;
  elem("mode").textContent = "Connecting";
  status("Connecting to the inference server…");
  display(null);
  try {
    const address = new URL(api.value);
    if (!["http:", "https:"].includes(address.protocol))
      throw new Error("Use an HTTP or HTTPS server URL.");
    endpoint = address.origin;
    const data = await request("/trips");
    trip.replaceChildren(...data.trip_ids.map((id) => new Option(id, id)));
    elem("mode").textContent =
      data.mode === "evaluator" ? "Evaluator mode" : "Student-test demo";
    sessionStorage.setItem("pathsnap.endpoint", endpoint);
    run.disabled = trip.disabled = !data.trip_ids.length;
    status(data.trip_ids.length + " trips available.");
  } catch (error) {
    trip.replaceChildren(new Option("Connect to a server"));
    elem("mode").textContent = "Offline";
    status("Could not connect. " + error.message, true);
  } finally {
    button.disabled = false;
  }
}

function display(data) {
  active = data;
  elem("accuracy").textContent =
    data?.accuracy == null ? "–" : (data.accuracy * 100).toFixed(2) + "%";
  elem("observations").textContent = data?.observations.toLocaleString() ?? "–";
  elem("segments").textContent =
    data?.route_arc_ids.length.toLocaleString() ?? "–";
  elem("duration").textContent = data
    ? (data.prediction_ms / 1000).toFixed(2) + " s"
    : "–";
  elem("placeholder").hidden = Boolean(data);
  elem("download").disabled = !data;
  elem("extent").textContent = data
    ? data.breaks.length + " route breaks · north is up"
    : "";
  draw();
}

function draw() {
  const { width, height } = canvas.getBoundingClientRect();
  const ratio = window.devicePixelRatio || 1;
  canvas.width = width * ratio;
  canvas.height = height * ratio;
  const ctx = canvas.getContext("2d");
  ctx.scale(ratio, ratio);
  ctx.strokeStyle = "#22372d";
  ctx.beginPath();
  for (let x = 20; x < width; x += 32) {
    ctx.moveTo(x, 0);
    ctx.lineTo(x, height);
  }
  for (let y = 20; y < height; y += 32) {
    ctx.moveTo(0, y);
    ctx.lineTo(width, y);
  }
  ctx.stroke();
  if (!active) return;
  let lx = Infinity,
    ly = Infinity,
    hx = -Infinity,
    hy = -Infinity;
  for (const [x, y] of active.gps.concat(active.route_segments.flat())) {
    lx = Math.min(lx, x);
    hx = Math.max(hx, x);
    ly = Math.min(ly, y);
    hy = Math.max(hy, y);
  }
  const cosine = Math.cos(((ly + hy) * Math.PI) / 360);
  const scale = Math.min(
    (width - 56) / Math.max((hx - lx) * cosine, 1e-8),
    (height - 56) / Math.max(hy - ly, 1e-8),
  );
  const pos = ([x, y]) => [
    width / 2 + (x - (lx + hx) / 2) * cosine * scale,
    height / 2 - (y - (ly + hy) / 2) * scale,
  ];
  if (elem("gps").checked) {
    ctx.fillStyle = "#67caff";
    for (const p of active.gps) {
      const [x, y] = pos(p);
      ctx.fillRect(x - 1.4, y - 1.4, 2.8, 2.8);
    }
  }
  if (elem("route").checked) {
    ctx.strokeStyle = "#b9f66a";
    ctx.lineWidth = 2.4;
    ctx.beginPath();
    for (const [a, b] of active.route_segments) {
      ctx.moveTo(...pos(a));
      ctx.lineTo(...pos(b));
    }
    ctx.stroke();
  }
}

elem("connection").addEventListener("submit", connect);
elem("inference").addEventListener("submit", async (event) => {
  event.preventDefault();
  const connection = elem("connection").querySelector("button");
  run.disabled = trip.disabled = connection.disabled = true;
  display(null);
  status("Reconstructing trip " + trip.value + "…");
  try {
    const result = await request("/match", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ trip_id: trip.value }),
    });
    display(result);
    status("Reconstructed trip " + result.trip_id + ".");
  } catch (error) {
    status("Reconstruction failed. " + error.message, true);
  } finally {
    run.disabled = trip.disabled = connection.disabled = false;
  }
});
elem("download").addEventListener("click", () => {
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(active)], { type: "application/json" }),
  );
  const link = Object.assign(document.createElement("a"), {
    href: url,
    download: "pathsnap-" + active.trip_id + ".json",
  });
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
for (const id of ["gps", "route"]) elem(id).addEventListener("change", draw);
new ResizeObserver(draw).observe(canvas);
api.value =
  new URLSearchParams(location.search).get("api") ||
  sessionStorage.getItem("pathsnap.endpoint") ||
  "http://localhost:8000";
connect();
