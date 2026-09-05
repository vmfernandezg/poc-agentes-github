# Reporte QA — FinCalc

Fecha: 2026-09-05  
Entorno: `http://localhost:8080` servido desde `web/`  
Método: ejecución en navegador real (Chromium vía Playwright local), con capturas en `qa/capturas/`.

| Caso | Esperado | Observado | Resultado |
|---|---|---|---|
| 1) Propina: cuenta 50, 10%, personas 2 | Propina 5,00 € · Total 55,00 € · Por persona 27,50 € | Propina 5,00 € · Total 55,00 € · Por persona 27,50 € (`qa/capturas/01-propina-calculo.png`) | ✅ |
| 2) Propina: botón 20% | Campo % pasa a 20 y botón resaltado | Campo `%` = `20` y botón `20%` activo/resaltado (`qa/capturas/02-propina-boton-20.png`) | ✅ |
| 3) Divisas: 100 EUR->USD | ≈ 108,00 $ | `108,00 US$` (`qa/capturas/03-divisas.png`) | ✅ |
| 4) Préstamo: 1200, 0%, 12 | Cuota 100,00 € · Total 1.200,00 € · Intereses 0,00 € | Cuota 100,00 € · Total 1200,00 € · Intereses 0,00 € (`qa/capturas/04-prestamo.png`) | ❌ |
| 5) Gastos: 120, 3, 0% | Total 120,00 € · Por persona 40,00 € | Total 120,00 € · Por persona 40,00 € (`qa/capturas/05-gastos.png`) | ✅ |
| 6) Ahorro: 1000, 100, 0% | 10 meses | `10 meses` (`qa/capturas/06-ahorro.png`) | ✅ |
| 7) Validación: Propina personas=0 | Se muestra error | Error visible: “El número de personas debe ser un entero de al menos 1.” (`qa/capturas/07-propina-invalido.png`) | ✅ |

## Resumen
- Casos ejecutados: 7/7  
- Correctos: 6  
- Fallos: 1

### Hallazgo principal
1. **Formato de miles en Préstamo (caso 4)**: el total mostrado es `1200,00 €` en lugar de `1.200,00 €` esperado.

## Notas UX / accesibilidad
- Los mensajes de error se muestran de forma clara y en línea con el formulario.
- Las pestañas y resultados son comprensibles visualmente.
- En divisas se muestra `US$` (formato localizado) en lugar de `$`; el valor numérico es correcto.
