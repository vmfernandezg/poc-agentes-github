import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
APP_JS = REPO_ROOT / "web" / "app.js"


class CalculadoraPropinaWebTests(unittest.TestCase):
    def test_por_persona_divide_el_total_entre_personas(self):
        script = f"""
const fs = require('fs');
const vm = require('vm');

const els = {{}};
function makeEl(id, value='') {{
  els[id] = {{
    value,
    textContent: '',
    classList: {{ add(){{}}, remove(){{}} }},
    addEventListener(){{}},
  }};
}}

['cuenta','porcentaje','personas','resultado','error','r-propina','r-total','r-persona','formulario']
  .forEach((id) => makeEl(id));

els.cuenta.value = '50';
els.porcentaje.value = '10';
els.personas.value = '2';

const context = {{
  document: {{ getElementById: (id) => els[id] }},
}};

vm.createContext(context);
vm.runInContext(fs.readFileSync('{APP_JS.as_posix()}', 'utf8'), context);
context.calcular({{ preventDefault() {{}} }});
process.stdout.write(els['r-persona'].textContent);
"""

        result = subprocess.run(
            ["node", "-e", script],
            capture_output=True,
            text=True,
            check=True,
            cwd=REPO_ROOT,
        )

        self.assertEqual(result.stdout.strip(), "27,50\u00a0€")


if __name__ == "__main__":
    unittest.main()
