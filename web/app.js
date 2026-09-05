// Lógica de la calculadora de propina.
//
// ⚠️ Contiene un BUG a propósito para la demo de agentes:
//    el "Total por persona" NO divide entre el número de personas.
//    Cuando un agente lo arregle (PR -> merge -> GitHub Pages redespliega),
//    verás el resultado corregido EN VIVO en la web.

const $ = (id) => document.getElementById(id);

function formatearEuros(n) {
  return n.toLocaleString("es-ES", { style: "currency", currency: "EUR" });
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

  const cuenta = parseFloat($("cuenta").value);
  const porcentaje = parseFloat($("porcentaje").value);
  const personas = parseInt($("personas").value, 10);

  // Validación básica de entradas.
  if (isNaN(cuenta) || cuenta <= 0) {
    mostrarError("Introduce un importe de cuenta válido.");
    return;
  }
  if (isNaN(porcentaje) || porcentaje < 0) {
    mostrarError("Introduce un porcentaje de propina válido.");
    return;
  }
  if (isNaN(personas) || personas < 1) {
    mostrarError("Debe haber al menos 1 persona.");
    return;
  }

  const propina = cuenta * (porcentaje / 100);
  const total = cuenta + propina;

  const porPersona = total / personas;

  $("error").classList.add("oculto");
  $("r-propina").textContent = formatearEuros(propina);
  $("r-total").textContent = formatearEuros(total);
  $("r-persona").textContent = formatearEuros(porPersona);
  $("resultado").classList.remove("oculto");
}

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
