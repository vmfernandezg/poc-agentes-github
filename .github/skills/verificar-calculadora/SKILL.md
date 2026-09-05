---
name: verificar-calculadora
description: Cómo probar la web FinCalc en un navegador real con Playwright — levantar el sitio en localhost, ejercitar las 5 calculadoras (propina, divisas, préstamo, gastos, ahorro), comprobar los resultados frente a valores esperados, capturar pantallas y redactar un informe de QA. Úsala para tareas de verificar, testear o hacer QA de la interfaz web.
---

# Verificar la interfaz de FinCalc

Playbook para comprobar que la web (`web/`) funciona de verdad en el navegador.

## 1. Levantar la web en local
El MCP de Playwright solo puede navegar a `localhost`/`127.0.0.1`, así que sirve la web:

```bash
cd web && python3 -m http.server 8080 &
```

La app queda en `http://localhost:8080`.

## 2. Abrir con Playwright y probar cada calculadora
Con el MCP de **Playwright**, navega a `http://localhost:8080`. Para cada módulo, cambia a
su pestaña, rellena los campos, pulsa el botón y **lee el resultado mostrado**. Compara con
lo esperado:

| Pestaña | Entradas | Resultado esperado |
|---|---|---|
| 💸 Propina | cuenta 50, propina 10%, personas 2 | Propina 5,00 € · Total 55,00 € · Por persona 27,50 € |
| 💸 Propina | pulsar botón "20%" | el campo % pasa a 20 y el botón queda resaltado |
| 💱 Divisas | 100, de EUR a USD | ≈ 108,00 $ (tasa 1 EUR = 1,08 USD) |
| 🏦 Préstamo | importe 1200, interés 0%, plazo 12 | Cuota 100,00 € · Total 1.200,00 € · Intereses 0,00 € |
| 🧾 Gastos | total 120, personas 3, propina 0% | Total 120,00 € · Por persona 40,00 € |
| 📈 Ahorro | meta 1000, aporte 100, interés 0% | 10 meses |

Comprueba también **un caso de validación** (p. ej. Propina con personas = 0 → debe
mostrarse el mensaje de error, no un resultado).

## 3. Capturas
Haz una captura de pantalla de cada pestaña con resultado visible y guárdalas en
`qa/capturas/` (créala si no existe). Inclúyelas en el Pull Request.

## 4. Informe
Crea `qa/REPORTE-QA.md` con:
- Una tabla: caso · esperado · observado · resultado (✅/❌).
- Un resumen (¿todo bien? ¿qué falló?).
- Cualquier problema de UX o accesibilidad que hayas notado.

## Notas
- No cambies la lógica de la app salvo un arreglo trivial y seguro; el objetivo es el informe.
- Si una API de Playwright no la tienes clara, consúltala en **Context7** antes de usarla.
- Detén el servidor al terminar si es necesario.
