// FinCalc — lógica de la mini-suite de calculadoras.
//
// Patrón: las funciones de CÁLCULO son PURAS (sin DOM) para poder testearlas con
// `node --test` (ver web/app.test.js). El cableado del DOM va aislado al final y solo
// se ejecuta en el navegador (guardado por `typeof document`).

// ----------------------------------------------------------------------------
//  Formato
// ----------------------------------------------------------------------------
function formatearEuros(n) {
  return n.toLocaleString("es-ES", { style: "currency", currency: "EUR" });
}

function formatearMoneda(n, moneda) {
  return n.toLocaleString("es-ES", { style: "currency", currency: moneda });
}

// ----------------------------------------------------------------------------
//  1) PROPINA  (se mantiene la API original: usada por los tests existentes)
// ----------------------------------------------------------------------------
function validarEntradas(cuenta, porcentaje, personas) {
  if (!Number.isFinite(cuenta) || cuenta <= 0) {
    return "Introduce un importe de cuenta válido.";
  }
  if (!Number.isFinite(porcentaje) || porcentaje < 0) {
    return "Introduce un porcentaje de propina válido.";
  }
  if (!Number.isFinite(personas) || !Number.isInteger(personas) || personas < 1) {
    return "El número de personas debe ser un entero de al menos 1.";
  }
  return null;
}

function calcularResumen(cuenta, porcentaje, personas) {
  const error = validarEntradas(cuenta, porcentaje, personas);
  if (error) return { error };

  const propina = cuenta * (porcentaje / 100);
  const total = cuenta + propina;
  const porPersona = total / personas;
  if (![propina, total, porPersona].every(Number.isFinite)) {
    return { error: "Los valores son demasiado grandes para calcularse con precisión." };
  }
  return { propina, total, porPersona };
}

// ----------------------------------------------------------------------------
//  2) DIVISAS
// ----------------------------------------------------------------------------
// Tasas de ejemplo: unidades de cada moneda por 1 EUR.
const TASAS = { EUR: 1, USD: 1.08, GBP: 0.85, JPY: 160, CHF: 0.95 };

function convertirDivisa(importe, origen, destino, tasas = TASAS) {
  if (!Number.isFinite(importe) || importe < 0) {
    return { error: "Introduce un importe válido." };
  }
  if (!tasas[origen] || !tasas[destino]) {
    return { error: "Moneda no reconocida." };
  }
  const enEuros = importe / tasas[origen];
  const resultado = enEuros * tasas[destino];
  const tasa = tasas[destino] / tasas[origen];
  return { resultado, tasa };
}

// ----------------------------------------------------------------------------
//  3) PRÉSTAMO  (cuota por sistema de amortización francés)
// ----------------------------------------------------------------------------
function cuotaPrestamo(principal, interesAnualPct, meses) {
  if (!Number.isFinite(principal) || principal <= 0) {
    return { error: "Introduce un importe de préstamo válido." };
  }
  if (!Number.isFinite(interesAnualPct) || interesAnualPct < 0) {
    return { error: "Introduce un interés válido (0 o mayor)." };
  }
  if (!Number.isFinite(meses) || !Number.isInteger(meses) || meses < 1) {
    return { error: "El plazo debe ser un número entero de meses (mínimo 1)." };
  }

  const r = interesAnualPct / 100 / 12;
  const cuota = r === 0 ? principal / meses : (principal * r) / (1 - Math.pow(1 + r, -meses));
  const totalPagado = cuota * meses;
  const intereses = totalPagado - principal;
  if (![cuota, totalPagado, intereses].every(Number.isFinite)) {
    return { error: "Los valores son demasiado grandes para calcularse." };
  }
  return { cuota, totalPagado, intereses };
}

// ----------------------------------------------------------------------------
//  4) DIVIDIR GASTOS
// ----------------------------------------------------------------------------
function dividirGastos(total, personas, propinaPct = 0) {
  if (!Number.isFinite(total) || total <= 0) {
    return { error: "Introduce un total de gasto válido." };
  }
  if (!Number.isFinite(personas) || !Number.isInteger(personas) || personas < 1) {
    return { error: "El número de personas debe ser un entero de al menos 1." };
  }
  if (!Number.isFinite(propinaPct) || propinaPct < 0) {
    return { error: "Introduce una propina válida (0 o mayor)." };
  }
  const totalConPropina = total * (1 + propinaPct / 100);
  const porPersona = totalConPropina / personas;
  return { totalConPropina, porPersona };
}

// ----------------------------------------------------------------------------
//  5) AHORRO OBJETIVO  (meses hasta alcanzar la meta con aporte mensual + interés)
// ----------------------------------------------------------------------------
function mesesAhorro(meta, aporteMensual, interesAnualPct) {
  if (!Number.isFinite(meta) || meta <= 0) {
    return { error: "Introduce una meta de ahorro válida." };
  }
  if (!Number.isFinite(aporteMensual) || aporteMensual <= 0) {
    return { error: "El aporte mensual debe ser mayor que 0." };
  }
  if (!Number.isFinite(interesAnualPct) || interesAnualPct < 0) {
    return { error: "Introduce un interés válido (0 o mayor)." };
  }

  const r = interesAnualPct / 100 / 12;
  const TOPE = 12000; // ~1000 años: cota de seguridad para no bucle infinito
  let saldo = 0;
  let meses = 0;
  while (saldo < meta && meses < TOPE) {
    saldo = saldo * (1 + r) + aporteMensual;
    meses += 1;
  }
  if (meses >= TOPE) {
    return { error: "Con esos datos la meta tardaría demasiado en alcanzarse." };
  }
  return { meses, anos: meses / 12 };
}

// ============================================================================
//  Cableado del DOM (solo navegador)
// ============================================================================
if (typeof document !== "undefined") {
  const $ = (id) => document.getElementById(id);

  // -- helper genérico: pinta error / resultado de un módulo --
  function mostrar(idResultado, idError, resultado, pintar) {
    const secResultado = $(idResultado);
    const secError = $(idError);
    if (resultado.error) {
      secResultado.classList.add("oculto");
      secError.textContent = resultado.error;
      secError.classList.remove("oculto");
      return;
    }
    secError.classList.add("oculto");
    pintar();
    secResultado.classList.remove("oculto");
  }

  // -------- Pestañas --------
  const tabs = document.querySelectorAll(".tab");
  function activarPanel(nombre) {
    document.querySelectorAll(".panel").forEach((p) => p.classList.add("oculto"));
    $("panel-" + nombre).classList.remove("oculto");
    tabs.forEach((t) => {
      const activa = t.dataset.panel === nombre;
      t.classList.toggle("activa", activa);
      t.setAttribute("aria-selected", String(activa));
    });
    try { localStorage.setItem("fincalc-tab", nombre); } catch (e) {}
  }
  tabs.forEach((t) => t.addEventListener("click", () => activarPanel(t.dataset.panel)));

  // -------- Tema claro/oscuro --------
  const botonTema = $("tema");
  function aplicarTema(tema) {
    document.documentElement.setAttribute("data-theme", tema);
    botonTema.textContent = tema === "dark" ? "☀️" : "🌙";
    try { localStorage.setItem("fincalc-tema", tema); } catch (e) {}
  }
  botonTema.addEventListener("click", () => {
    const actual = document.documentElement.getAttribute("data-theme");
    aplicarTema(actual === "dark" ? "light" : "dark");
  });

  // -------- 1) Propina --------
  function actualizarBotonActivo(valor) {
    const porcentaje = Number(valor);
    document.querySelectorAll(".boton-propina").forEach((boton) => {
      const activo = Number(boton.dataset.porcentaje) === porcentaje;
      boton.classList.toggle("activo", activo);
      boton.setAttribute("aria-pressed", String(activo));
    });
  }
  document.querySelectorAll(".boton-propina").forEach((boton) => {
    boton.addEventListener("click", () => {
      $("porcentaje").value = boton.dataset.porcentaje;
      actualizarBotonActivo(boton.dataset.porcentaje);
    });
  });
  $("porcentaje").addEventListener("input", (e) => actualizarBotonActivo(e.target.value));
  actualizarBotonActivo($("porcentaje").value);
  $("formulario").addEventListener("submit", (e) => {
    e.preventDefault();
    const r = calcularResumen(Number($("cuenta").value), Number($("porcentaje").value), Number($("personas").value));
    mostrar("resultado", "error", r, () => {
      $("r-propina").textContent = formatearEuros(r.propina);
      $("r-total").textContent = formatearEuros(r.total);
      $("r-persona").textContent = formatearEuros(r.porPersona);
    });
  });

  // -------- 2) Divisas --------
  $("form-divisas").addEventListener("submit", (e) => {
    e.preventDefault();
    const origen = $("div-origen").value;
    const destino = $("div-destino").value;
    const r = convertirDivisa(Number($("div-importe").value), origen, destino);
    mostrar("div-resultado", "div-error", r, () => {
      $("div-r-total").textContent = formatearMoneda(r.resultado, destino);
      $("div-r-tasa").textContent = `1 ${origen} = ${r.tasa.toLocaleString("es-ES", { maximumFractionDigits: 4 })} ${destino}`;
    });
  });

  // -------- 3) Préstamo --------
  $("form-prestamo").addEventListener("submit", (e) => {
    e.preventDefault();
    const r = cuotaPrestamo(Number($("pre-importe").value), Number($("pre-interes").value), Number($("pre-meses").value));
    mostrar("pre-resultado", "pre-error", r, () => {
      $("pre-r-cuota").textContent = formatearEuros(r.cuota);
      $("pre-r-total").textContent = formatearEuros(r.totalPagado);
      $("pre-r-intereses").textContent = formatearEuros(r.intereses);
    });
  });

  // -------- 4) Dividir gastos --------
  $("form-gastos").addEventListener("submit", (e) => {
    e.preventDefault();
    const r = dividirGastos(Number($("gas-total").value), Number($("gas-personas").value), Number($("gas-propina").value));
    mostrar("gas-resultado", "gas-error", r, () => {
      $("gas-r-total").textContent = formatearEuros(r.totalConPropina);
      $("gas-r-persona").textContent = formatearEuros(r.porPersona);
    });
  });

  // -------- 5) Ahorro --------
  $("form-ahorro").addEventListener("submit", (e) => {
    e.preventDefault();
    const r = mesesAhorro(Number($("aho-meta").value), Number($("aho-aporte").value), Number($("aho-interes").value));
    mostrar("aho-resultado", "aho-error", r, () => {
      const anos = Math.floor(r.meses / 12);
      const restoMeses = r.meses % 12;
      const partes = [];
      if (anos > 0) partes.push(`${anos} año${anos !== 1 ? "s" : ""}`);
      if (restoMeses > 0) partes.push(`${restoMeses} mes${restoMeses !== 1 ? "es" : ""}`);
      $("aho-r-tiempo").textContent = partes.join(" y ") || "menos de 1 mes";
      $("aho-r-meses").textContent = String(r.meses);
    });
  });

  // -------- Restaurar preferencias --------
  try {
    aplicarTema(localStorage.getItem("fincalc-tema") === "dark" ? "dark" : "light");
    const tabGuardada = localStorage.getItem("fincalc-tab");
    if (tabGuardada && $("panel-" + tabGuardada)) activarPanel(tabGuardada);
  } catch (e) {}
}

// ============================================================================
//  Exports para los tests (node --test)
// ============================================================================
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    formatearEuros,
    validarEntradas,
    calcularResumen,
    convertirDivisa,
    cuotaPrestamo,
    dividirGastos,
    mesesAhorro,
    TASAS,
  };
}
