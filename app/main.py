from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.logic import comparator_math, farm_plan, gate_truth_table, timing_summary

app = FastAPI(title="Sophie Redstone Studio", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class GateRequest(BaseModel):
    gate: str
    inputs: list[int] = [0, 0]


class ComparatorRequest(BaseModel):
    signal: int
    threshold: int


class TimingRequest(BaseModel):
    repeater_delay_ticks: int
    pulses: int
    period_ticks: int | None = None


class FarmRequest(BaseModel):
    farm_type: str


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "name": "Sophie Redstone Studio"}


@app.post("/api/redstone/gate")
def redstone_gate(request: GateRequest) -> dict:
    return gate_truth_table(request.gate, request.inputs)


@app.post("/api/redstone/comparator")
def redstone_comparator(request: ComparatorRequest) -> dict:
    return comparator_math(request.signal, request.threshold)


@app.post("/api/redstone/timing")
def redstone_timing(request: TimingRequest) -> dict:
    return timing_summary(request.repeater_delay_ticks, request.pulses, request.period_ticks)


@app.post("/api/farm/plan")
def farm(request: FarmRequest) -> dict:
    return farm_plan(request.farm_type)


@app.get("/")
def root() -> str:
    return """<!doctype html>
    <html lang=\"en\">
      <head>
        <meta charset=\"utf-8\" />
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
        <title>Sophie Redstone Studio</title>
        <style>
          body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #10131a;
            color: #edf3ff;
          }
          .container {
            max-width: 960px;
            margin: 0 auto;
            padding: 32px 20px 64px;
          }
          .card {
            background: #171d2a;
            border: 1px solid #2b3850;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
          }
          label, select, input, button {
            display: block;
            width: 100%;
            margin-top: 8px;
            box-sizing: border-box;
          }
          input, select, button {
            padding: 10px 12px;
            border-radius: 8px;
            border: 1px solid #364a73;
            background: #0f1523;
            color: #edf3ff;
          }
          button {
            background: linear-gradient(135deg, #2d7dff, #00b7ff);
            border: none;
            font-weight: bold;
            cursor: pointer;
          }
          .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
          }
          pre {
            white-space: pre-wrap;
            background: #0d1320;
            border-radius: 8px;
            padding: 12px;
            overflow: auto;
          }
        </style>
      </head>
      <body>
        <div class=\"container\">
          <h1>Sophie Redstone Studio</h1>
          <p>Desktop-style utility for redstone logic, timing, and farm planning.</p>

          <div class=\"grid\">
            <div class=\"card\">
              <h2>Redstone gate</h2>
              <label>Gate
                <select id=\"gate\">
                  <option value=\"AND\">AND</option>
                  <option value=\"OR\">OR</option>
                  <option value=\"XOR\">XOR</option>
                  <option value=\"NAND\">NAND</option>
                  <option value=\"NOR\">NOR</option>
                  <option value=\"NOT\">NOT</option>
                </select>
              </label>
              <label>Inputs (comma-separated)
                <input id=\"inputs\" value=\"1,1\" />
              </label>
              <button id=\"gateBtn\">Calculate</button>
              <pre id=\"gateResult\"></pre>
            </div>

            <div class=\"card\">
              <h2>Comparator math</h2>
              <label>Signal
                <input id=\"signal\" type=\"number\" value=\"12\" />
              </label>
              <label>Threshold
                <input id=\"threshold\" type=\"number\" value=\"9\" />
              </label>
              <button id=\"compareBtn\">Check</button>
              <pre id=\"compareResult\"></pre>
            </div>

            <div class=\"card\">
              <h2>Timing</h2>
              <label>Repeater delay (ticks)
                <input id=\"delay\" type=\"number\" value=\"1\" />
              </label>
              <label>Pulses
                <input id=\"pulses\" type=\"number\" value=\"4\" />
              </label>
              <button id=\"timingBtn\">Estimate</button>
              <pre id=\"timingResult\"></pre>
            </div>

            <div class=\"card\">
              <h2>Farm plan</h2>
              <label>Farm type
                <select id=\"farmType\">
                  <option value=\"mob\">Mob grinder</option>
                  <option value=\"iron\">Iron farm</option>
                  <option value=\"gold\">Gold farm</option>
                  <option value=\"villager\">Villager breeder</option>
                  <option value=\"crop\">Crop farm</option>
                </select>
              </label>
              <button id=\"farmBtn\">Generate plan</button>
              <pre id=\"farmResult\"></pre>
            </div>
          </div>
        </div>

        <script>
          async function callJson(path, body) {
            const res = await fetch(path, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(body)
            });
            return await res.json();
          }

          document.getElementById('gateBtn').addEventListener('click', async () => {
            const inputs = document.getElementById('inputs').value.split(',').map(v => Number(v.trim()));
            const result = await callJson('/api/redstone/gate', { gate: document.getElementById('gate').value, inputs });
            document.getElementById('gateResult').textContent = JSON.stringify(result, null, 2);
          });

          document.getElementById('compareBtn').addEventListener('click', async () => {
            const result = await callJson('/api/redstone/comparator', {
              signal: Number(document.getElementById('signal').value),
              threshold: Number(document.getElementById('threshold').value)
            });
            document.getElementById('compareResult').textContent = JSON.stringify(result, null, 2);
          });

          document.getElementById('timingBtn').addEventListener('click', async () => {
            const result = await callJson('/api/redstone/timing', {
              repeater_delay_ticks: Number(document.getElementById('delay').value),
              pulses: Number(document.getElementById('pulses').value)
            });
            document.getElementById('timingResult').textContent = JSON.stringify(result, null, 2);
          });

          document.getElementById('farmBtn').addEventListener('click', async () => {
            const result = await callJson('/api/farm/plan', {
              farm_type: document.getElementById('farmType').value
            });
            document.getElementById('farmResult').textContent = JSON.stringify(result, null, 2);
          });
        </script>
      </body>
    </html>
    """


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
