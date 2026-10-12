"""writes 45.html, 55.html, 57.html: one simple 3D viewer per knot (three.js), with its braid word and root"""
import os

D = os.path.dirname(os.path.abspath(__file__))
KNOTS = {
    "45": ([3, -2, 3, -2, 3, 3, -2, -2, -2, -2, 1, 1, 1, -2, -2], 4, 3, "−1.0810 ± 1.5924i", "(σ₃σ₂⁻¹σ₃σ₂⁻¹σ₃²σ₂⁻⁴σ₁³σ₂⁻²)³"),
    "55": ([1, 1, -2, -2, -2, 3, -2, 3, -2, -2, 1], 4, 5, "−1.1235 ± 1.3560i", "(σ₁²σ₂⁻³σ₃σ₂⁻¹σ₃σ₂⁻²σ₁)⁵"),
    "57": ([3, -2, -2, -2, -2, -2, 1, 1, 1, -2, -2, -2, -2, -2, -2, 3, 3, 3, 3], 4, 3, "−1.1909 ± 1.4154i", "(σ₃σ₂⁻⁵σ₁³σ₂⁻⁶σ₃⁴)³"),
}
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
