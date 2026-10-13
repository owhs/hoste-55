"""one simple 3D viewer per knot (three.js), for EVERY k*_certificate.json in this folder: writes <crossings>.html with
the braid word and root, and index.html linking them all. Add a certificate, rerun, and its page appears.
Run: python make_viewers.py"""
import glob
import itertools
import json
import os
import re

D = os.path.dirname(os.path.abspath(__file__))
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def word_text(block, reps):
    """[1, 1, -2, 3] , 5 -> (σ₁²σ₂⁻¹σ₃)⁵"""
    out = ""
    for g, run in itertools.groupby(block):
        e = len(list(run)) * (1 if g > 0 else -1)
        out += "σ" + str(abs(g)).translate(SUB) + ("" if e == 1 else str(e).translate(SUP))
    return out if reps == 1 else f"({out})" + str(reps).translate(SUP)


def root_text(s):
    """'(-1.0747... + 1.7916...j)' -> '−1.0747 ± 1.7916i'"""
    x, y = (float(v) for v in re.findall(r"[-+]?\d+\.\d+", s.replace(" ", ""))[:2])
    return f"{x:.4f} ± {abs(y):.4f}i".replace("-", "−")


KNOTS = {}
for p in glob.glob(os.path.join(D, "k*_certificate.json")):
    c = json.load(open(p, encoding="utf-8"))
    KNOTS[str(c["crossings"])] = (c["block"], c["strands"], c["repeats"], root_text(c["refined_root"]),
                                  word_text(c["block"], c["repeats"]))
KNOTS = dict(sorted(KNOTS.items(), key=lambda kv: int(kv[0])))
TEMPLATE = """<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>K__N__</title>
<style>html,body{margin:0;height:100%;background:#0b0d12;color:#e7e2d6;font:14px/1.5 ui-monospace,Consolas,monospace}
canvas{display:block}#cap{position:fixed;left:16px;bottom:16px;max-width:calc(100% - 32px);pointer-events:none}
#cap b{font-size:18px;color:#fff}#cap .r{color:#ee5f73}</style></head>
<body>
<div id="cap"><b>__N__-crossing alternating knot</b><br>__WORD__ on __S__ strands<br>Alexander roots <span class="r">__ROOT__</span>, past Re = −1 (Hoste's line)</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script>
const block = __BLOCK__, strands = __S__, reps = __REPS__;
const word = Array(reps).fill(block).flat();
const pts = [], R = 3, gap = 0.5, lift = 0.25, steps = 12, L = word.length;
let p = 0;
for (let pass = 0; pass < strands; pass++) {
  for (let k = 0; k < L; k++) {
    const g = word[k], i = Math.abs(g) - 1, moving = p === i || p === i + 1;
    const to = moving ? (p === i ? i + 1 : i) : p;
    const over = moving && ((g > 0) === (p === i));
    for (let s = 0; s < steps; s++) {
      const u = s / steps, e = 0.5 - 0.5 * Math.cos(Math.PI * u);
      const ang = 2 * Math.PI * (k + u) / L;
      const r = R + gap * ((p + (to - p) * e) - (strands - 1) / 2);
      const y = moving ? (over ? 1 : -1) * lift * Math.sin(Math.PI * u) : 0;
      pts.push(new THREE.Vector3(r * Math.cos(ang), y, r * Math.sin(ang)));
    }
    p = to;
  }
  if (p === 0) break;
}
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, innerWidth / innerHeight, 0.1, 100);
camera.position.set(0, 7, 8);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(innerWidth, innerHeight);
renderer.setPixelRatio(devicePixelRatio);
document.body.appendChild(renderer.domElement);
const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
scene.add(new THREE.HemisphereLight(0xffffff, 0x223344, 0.7));
const sun = new THREE.DirectionalLight(0xffffff, 0.8); sun.position.set(5, 10, 7); scene.add(sun);
const curve = new THREE.CatmullRomCurve3(pts, true, 'centripetal');
const tube = new THREE.Mesh(new THREE.TubeGeometry(curve, pts.length * 2, 0.08, 12, true),
  new THREE.MeshStandardMaterial({ color: 0xf1c35f, roughness: 0.35, metalness: 0.2 }));
scene.add(tube);
addEventListener('resize', () => { camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix(); renderer.setSize(innerWidth, innerHeight); });
(function loop() { tube.rotation.y += 0.002; controls.update(); renderer.render(scene, camera); requestAnimationFrame(loop); })();
</script>
</body></html>
"""
for n, (block, s, reps, root, word) in KNOTS.items():
    html = (TEMPLATE.replace("__N__", n).replace("__WORD__", word).replace("__S__", str(s)).replace("__ROOT__", root)
            .replace("__BLOCK__", str(block)).replace("__REPS__", str(reps)))
    with open(os.path.join(D, f"{n}.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"{n}.html")

rows = "\n".join(f'<li><a href="{n}.html"><b>K{n}</b></a> {w} on {s} strands, roots <span class="r">{r}</span></li>'
                 for n, (_b, s, _k, r, w) in KNOTS.items())
with open(os.path.join(D, "index.html"), "w", encoding="utf-8") as f:
    f.write(f"""<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Hoste counterexamples</title>
<style>body{{margin:0;padding:24px 16px;background:#0b0d12;color:#e7e2d6;font:15px/1.7 ui-monospace,Consolas,monospace}}
a{{color:#f1c35f}}.r{{color:#ee5f73}}ul{{padding-left:20px}}</style></head>
<body><h1 style="font-size:20px">Alternating knots with Alexander roots past Re = −1</h1>
<p>Counterexamples to Hoste's conjecture. Click a knot to see it in 3D; <code>python verify.py all</code> checks them.</p>
<ul>
{rows}
</ul></body></html>
""")
print("index.html")
