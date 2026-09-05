// Lógica de la calculadora de propina.
//
// Cálculo y validación de la calculadora de propina.

const $ = (id) => document.getElementById(id);

function formatearEuros(n) {
  return n.toLocaleString("es-ES", { style: "currency", currency: "EUR" });
}

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
  if (error) {
    return { error };
  }

  const propina = cuenta * (porcentaje / 100);
  const total = cuenta + propina;
  const porPersona = total / personas;
  if (!Number.isFinite(propina) || !Number.isFinite(total) || !Number.isFinite(porPersona)) {
    return { error: "Los valores son demasiado grandes para calcularse con precisión." };
  }
  return { propina, total, porPersona };
}

function mostrarError(mensaje) {
  $("resultado").classList.add("oculto");
  const err = $("error");
  err.textContent = mensaje;
  err.classList.remove("oculto");
}

function actualizarBotonActivo(valor) {
  const porcentaje = Number(valor);
  document.querySelectorAll(".boton-propina").forEach((boton) => {
    const activo = Number(boton.dataset.porcentaje) === porcentaje;
    boton.classList.toggle("activo", activo);
    boton.setAttribute("aria-pressed", String(activo));
  });
}

function calcular(evento) {
  evento.preventDefault();

  const cuenta = Number($("cuenta").value);
  const porcentaje = Number($("porcentaje").value);
  const personas = Number($("personas").value);

  const resumen = calcularResumen(cuenta, porcentaje, personas);
  if (resumen.error) {
    mostrarError(resumen.error);
    return;
  }

  $("error").classList.add("oculto");
  $("r-propina").textContent = formatearEuros(resumen.propina);
  $("r-total").textContent = formatearEuros(resumen.total);
  $("r-persona").textContent = formatearEuros(resumen.porPersona);
  $("resultado").classList.remove("oculto");
}

if (typeof document !== "undefined") {
  document.querySelectorAll(".boton-propina").forEach((boton) => {
    boton.addEventListener("click", () => {
      $("porcentaje").value = boton.dataset.porcentaje;
      actualizarBotonActivo(boton.dataset.porcentaje);
    });
  });

  $("porcentaje").addEventListener("input", (evento) => {
    actualizarBotonActivo(evento.target.value);
  });

  actualizarBotonActivo($("porcentaje").value);
  document.getElementById("formulario").addEventListener("submit", calcular);
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { formatearEuros, validarEntradas, calcularResumen };
}
